import pytest
from mock import Mock, patch, call
from pyramid.security import (
    Allow, Deny,
    Everyone, Authenticated,
    ALL_PERMISSIONS)

from ramses import acl


class TestACLHelpers(object):
    methods_map = {'get': 'index', 'post': 'create'}

    def test_methods_to_perms_all_permissions(self):
        perms = acl.methods_to_perms('all,get,post', self.methods_map)
        assert perms is ALL_PERMISSIONS

    def test_methods_to_perms_invalid_perm_name(self):
        with pytest.raises(ValueError) as ex:
            acl.methods_to_perms('foo,post', self.methods_map)
        expected = ("Unknown method name in permissions: "
                    "['foo', 'post']")
        assert expected in str(ex.value)

    def test_methods_to_perms(self):
        perms = acl.methods_to_perms('get', self.methods_map)
        assert perms == ['view']
        perms = acl.methods_to_perms('get,post', self.methods_map)
        assert sorted(perms) == ['create', 'view']

    def test_parse_acl_no_string(self):
        perms = acl.parse_acl('', self.methods_map)
        assert perms == [acl.ALLOW_ALL]

    def test_parse_acl_unknown_action(self):
        with pytest.raises(ValueError) as ex:
            acl.parse_acl('foobar admin all', self.methods_map)
        assert 'Unknown ACL action: foobar' in str(ex.value)

    @patch.object(acl, 'methods_to_perms')
    def test_parse_acl_multiple_values(self, mock_perms):
        mock_perms.return_value = 'Foo'
        perms = acl.parse_acl(
            'allow everyone read,write;allow authenticated all',
            self.methods_map)
        mock_perms.assert_has_calls([
            call(['read', 'write'], self.methods_map),
            call(['all'], self.methods_map),
        ])
        assert sorted(perms) == sorted([
            (Allow, Everyone, 'Foo'),
            (Allow, Authenticated, 'Foo'),
        ])

    @patch.object(acl, 'methods_to_perms')
    def test_parse_acl_special_principal(self, mock_perms):
        mock_perms.return_value = 'Foo'
        perms = acl.parse_acl('allow everyone all', self.methods_map)
        mock_perms.assert_called_once_with(['all'], self.methods_map)
        assert perms == [(Allow, Everyone, 'Foo')]

    @patch.object(acl, 'methods_to_perms')
    def test_parse_acl_group_principal(self, mock_perms):
        mock_perms.return_value = 'Foo'
        perms = acl.parse_acl('allow admin all', self.methods_map)
        mock_perms.assert_called_once_with(['all'], self.methods_map)
        assert perms == [(Allow, 'g:admin', 'Foo')]

    @patch.object(acl, 'resolve_to_callable')
    @patch.object(acl, 'methods_to_perms')
    def test_parse_acl_callable_principal(self, mock_perms, mock_res):
        mock_perms.return_value = 'Foo'
        mock_res.return_value = 'registry callable'
        perms = acl.parse_acl('allow {{my_user}} all', self.methods_map)
        mock_perms.assert_called_once_with(['all'], self.methods_map)
        mock_res.assert_called_once_with('{{my_user}}')
        assert perms == [(Allow, 'registry callable', 'Foo')]


@patch.object(acl, 'parse_acl')
class TestGenerateACL(object):

    def test_no_security(self, mock_parse):
        acl_cls = acl.generate_acl(
            model_cls='Foo',
            raml_resource=Mock(security_schemes=[]),
            es_based=True)
        assert acl_cls.item_model == 'Foo'
        assert issubclass(acl_cls, acl.BaseACL)
        instance = acl_cls(request=None)
        assert instance.es_based
        assert instance._collection_acl == [acl.ALLOW_ALL]
        assert instance._item_acl == [acl.ALLOW_ALL]
        assert not mock_parse.called

    def test_wrong_security_scheme_type(self, mock_parse):
        raml_resource = Mock(security_schemes=[
            Mock(type='x-Foo', settings={'collection': 4, 'item': 7})
        ])
        acl_cls = acl.generate_acl(
            model_cls='Foo',
            raml_resource=raml_resource,
            es_based=False)
        assert not mock_parse.called
        assert acl_cls.item_model == 'Foo'
        assert issubclass(acl_cls, acl.BaseACL)
        instance = acl_cls(request=None)
        assert not instance.es_based
        assert instance._collection_acl == [acl.ALLOW_ALL]
        assert instance._item_acl == [acl.ALLOW_ALL]

    def test_correct_security_scheme(self, mock_parse):
        raml_resource = Mock(security_schemes=[
            Mock(type='x-ACL', settings={'collection': 4, 'item': 7})
        ])
        acl_cls = acl.generate_acl(
            model_cls='Foo',
            raml_resource=raml_resource,
            es_based=False)
        mock_parse.assert_has_calls([
            call(acl_string=4, methods_map=acl.collection_methods),
            call(acl_string=7, methods_map=acl.item_methods),
        ])
        instance = acl_cls(request=None)
        assert instance._collection_acl == mock_parse()
        assert instance._item_acl == mock_parse()
        assert not instance.es_based


class TestBaseACL(object):

    def test_init(self):
        obj = acl.BaseACL(request='Foo')
        assert obj.item_model is None
        assert obj._collection_acl == (acl.ALLOW_ALL,)
        assert obj._item_acl == (acl.ALLOW_ALL,)
        assert obj.request == 'Foo'

    def test_apply_callables_no_callables(self):
        obj = acl.BaseACL('req')
        new_acl = obj._apply_callables(
            acl=[('foo', 'bar', 'baz')],
            methods_map={'zoo': 1},
            obj='obj')
        assert new_acl == [('foo', 'bar', 'baz')]

    @patch.object(acl, 'methods_to_perms')
    def test_apply_callables(self, mock_meth):
        mock_meth.return_value = '123'
        principal = Mock(return_value=(7, 8, 9))
        obj = acl.BaseACL('req')
        new_acl = obj._apply_callables(
            acl=[('foo', principal, 'bar')],
            methods_map={'zoo': 1},
            obj='obj')
        assert new_acl == [(7, 8, '123')]
        principal.assert_called_once_with(
            ace=('foo', principal, 'bar'),
            request='req',
            obj='obj')
        mock_meth.assert_called_once_with(9, {'zoo': 1})

    @patch.object(acl, 'methods_to_perms')
    def test_apply_callables_principal_returns_none(self, mock_meth):
        mock_meth.return_value = '123'
        principal = Mock(return_value=None)
        obj = acl.BaseACL('req')
        new_acl = obj._apply_callables(
            acl=[('foo', principal, 'bar')],
            methods_map={'zoo': 1},
            obj='obj')
        assert new_acl == []
        principal.assert_called_once_with(
            ace=('foo', principal, 'bar'),
            request='req',
            obj='obj')
        assert not mock_meth.called

    @patch.object(acl, 'methods_to_perms')
    def test_apply_callables_principal_returns_list(self, mock_meth):
        mock_meth.return_value = '123'
        principal = Mock(return_value=[(7, 8, 9)])
        obj = acl.BaseACL('req')
        new_acl = obj._apply_callables(
            acl=[('foo', principal, 'bar')],
            methods_map={'zoo': 1},
            obj='obj')
        assert new_acl == [(7, 8, '123')]
        principal.assert_called_once_with(
            ace=('foo', principal, 'bar'),
            request='req',
            obj='obj')
        mock_meth.assert_called_once_with(9, {'zoo': 1})

    def test_apply_callables_functional(self):
        obj = acl.BaseACL('req')
        principal = lambda ace, request, obj: [(Allow, Everyone, 'get')]
        new_acl = obj._apply_callables(
            acl=[(Deny, principal, ALL_PERMISSIONS)],
            methods_map=acl.item_methods,
        )
        assert new_acl == [(Allow, Everyone, ['view'])]

    def test_magic_acl(self):
        obj = acl.BaseACL('req')
        obj._collection_acl = [(1, 2, 3)]
        obj._apply_callables = Mock()
        result = obj.__acl__()
        obj._apply_callables.assert_called_once_with(
            acl=[(1, 2, 3)],
            methods_map=acl.collection_methods
        )
        assert result == obj._apply_callables()

    def test_item_acl(self):
        obj = acl.BaseACL('req')
        obj._item_acl = [(1, 2, 3)]
        obj._apply_callables = Mock()
        result = obj.item_acl('foobar')
        obj._apply_callables.assert_called_once_with(
            acl=[(1, 2, 3)],
            methods_map=acl.item_methods,
            obj='foobar'
        )
        assert result == obj._apply_callables()

    def test_magic_getitem_es_based(self):
        obj = acl.BaseACL('req')
        obj.item_db_id = Mock(return_value=42)
        obj.getitem_es = Mock()
        obj.es_based = True
        obj.__getitem__(1)
        obj.item_db_id.assert_called_once_with(1)
        obj.getitem_es.assert_called_once_with(42)

    def test_magic_getitem_db_based(self):
        obj = acl.BaseACL('req')
        obj.item_db_id = Mock(return_value = 42)
        obj.item_model = Mock()
        obj.item_model.pk_field.return_value = 'id'
        obj.es_based = False
        obj.__getitem__(1)
        obj.item_db_id.assert_called_once_with(1)

    def test_getitem_db(self):
        obj = acl.BaseACL('req')
        obj.item_model = Mock()
        obj.item_model.pk_field.return_value = 'myname'
        obj.item_acl = Mock()
        value = obj['varvar']
        obj.item_model.get.assert_called_once_with(
            __raise=True, myname='varvar')
        obj.item_acl.assert_called_once_with(
            obj.item_model.get())
        assert value.__acl__ == obj.item_acl()
        assert value.__parent__ is obj
        assert value.__name__ == 'varvar'

    @patch('ramses.acl.ES')
    def test_getitem_es(self, mock_es):
        found_obj = Mock()
        es_obj = Mock()
        es_obj.get_resource.return_value = found_obj
        mock_es.return_value = es_obj
        obj = acl.BaseACL('req')
        obj.item_model = Mock(__name__='Foo')
        obj.item_model.pk_field.return_value = 'myname'
        obj.item_acl = Mock()
        value = obj.getitem_es(key='varvar')
        mock_es.assert_called_with('Foo')
        es_obj.get_resource.assert_called_once_with(id='varvar')
        obj.item_acl.assert_called_once_with(found_obj)
        assert value.__acl__ == obj.item_acl()
        assert value.__parent__ is obj
        assert value.__name__ == 'varvar'
