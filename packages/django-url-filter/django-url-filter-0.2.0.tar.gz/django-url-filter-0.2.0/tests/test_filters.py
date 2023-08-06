# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from functools import partial

import mock
import pytest
from django import forms

from url_filter.backends.django import DjangoFilterBackend
from url_filter.fields import MultipleValuesField
from url_filter.filters import Filter as _Filter
from url_filter.utils import FilterSpec, LookupConfig


Filter = partial(_Filter, lookups=DjangoFilterBackend.supported_lookups)


class TestFilter(object):
    def test_init(self):
        f = Filter(
            source='foo',
            form_field=forms.CharField(),
            lookups=['foo', 'bar'],
            default_lookup='foo',
            is_default=True,
        )

        assert f.source == 'foo'
        assert isinstance(f.form_field, forms.CharField)
        assert f.lookups == {'foo', 'bar'}
        assert f.default_lookup == 'foo'
        assert f.is_default is True
        assert f.parent is None
        assert f.name is None

    def test_lookups(self):
        assert Filter(form_field=None, lookups=['foo', 'bar']).lookups == {'foo', 'bar'}
        assert Filter(form_field=None, lookups=None).lookups == set()

        f = Filter(form_field=None, lookups=None)
        f.parent = mock.Mock()
        f.parent.root = f.parent
        f.parent.filter_backend.supported_lookups = DjangoFilterBackend.supported_lookups

        assert f.lookups == DjangoFilterBackend.supported_lookups

    def test_repr(self):
        f = Filter(
            source='foo',
            lookups=None,
            form_field=forms.CharField(),
            default_lookup='foo',
            is_default=True,
        )

        assert repr(f) == (
            'Filter(form_field=CharField, lookups=ALL, '
            'default_lookup="foo", is_default=True)'
        )

    def test_source(self):
        f = Filter(source=None, form_field=forms.CharField())
        f.name = 'bar'

        assert f.source == 'bar'
        assert Filter(source='foo', form_field=forms.CharField()).source == 'foo'

    def test_components(self):
        p = Filter(source='parent', form_field=forms.CharField())
        f = Filter(source='child', form_field=forms.CharField())

        assert f.components == []
        f.parent = p
        assert f.components == ['child']

    def test_bind(self):
        f = Filter(form_field=forms.CharField())
        f.bind('foo', 'parent')

        assert f.name == 'foo'
        assert f.parent == 'parent'

    def test_root(self):
        p = Filter(source='parent', form_field=forms.CharField())
        f = Filter(source='child', form_field=forms.CharField())
        f.parent = p

        assert f.root is p

    def test_get_form_field(self):
        f = Filter(form_field=forms.CharField())

        assert isinstance(f.get_form_field('exact'), forms.CharField)
        assert isinstance(f.get_form_field('in'), MultipleValuesField)
        assert isinstance(f.get_form_field('isnull'), forms.BooleanField)

    def test_clean_value(self):
        f = Filter(form_field=forms.IntegerField())

        assert f.clean_value('5', 'exact') == 5

        with pytest.raises(forms.ValidationError):
            f.clean_value('a', 'exact')

    def test_get_spec(self):
        p = Filter(source='parent', form_field=forms.CharField())
        f = Filter(source='child', form_field=forms.CharField())
        f.parent = p

        assert f.get_spec(LookupConfig('key', 'value')) == FilterSpec(
            ['child'], 'exact', 'value', False
        )
        assert f.get_spec(LookupConfig('key!', 'value')) == FilterSpec(
            ['child'], 'exact', 'value', True
        )
        assert f.get_spec(LookupConfig('key', {'contains': 'value'})) == FilterSpec(
            ['child'], 'contains', 'value', False
        )

        with pytest.raises(forms.ValidationError):
            assert f.get_spec(LookupConfig('key', {'foo': 'value'}))
        with pytest.raises(forms.ValidationError):
            assert f.get_spec(LookupConfig('key', {
                'foo': 'value', 'happy': 'rainbows',
            }))
