# coding: utf-8

from __future__ import unicode_literals

import copy

import requests
import webbrowser

from .exceptions import ResponseProcessException


class TapiocaInstantiator(object):

    def __init__(self, adapter_class):
        self.adapter_class = adapter_class

    def __call__(self, *args, **kwargs):
        return TapiocaClient(self.adapter_class(), api_params=kwargs)


class TapiocaClient(object):

    def __init__(self, api, data=None, response=None, request_kwargs=None,
                 api_params={}, resource=None, *args, **kwargs):
        self._api = api
        self._data = data
        self._response = response
        self._api_params = api_params
        self._request_kwargs = request_kwargs
        self._resource = resource

    def _get_doc(self):
        resources = copy.copy(self._resource)
        docs = ("Automatic generated __doc__ from resource_mapping.\n"
                "Resource: %s\n"
                "Docs: %s\n" % (resources.pop('resource', ''),
                                resources.pop('docs', '')))
        for key, value in sorted(resources.items()):
            docs += "%s: %s\n" % (key.title(), value)
        docs = docs.strip()
        return docs

    __doc__ = property(_get_doc)

    def __call__(self, *args, **kwargs):
        data = self._data
        if kwargs:
            data = self._api.fill_resource_template_url(self._data, kwargs)

        return TapiocaClientExecutor(self._api.__class__(), data=data, api_params=self._api_params,
            resource=self._resource, response=self._response)

    def _get_client_from_name(self, name):
        if self._data and \
            ((isinstance(self._data, list) and isinstance(name, int)) or \
                (hasattr(self._data, '__iter__') and name in self._data)):
            return TapiocaClient(self._api.__class__(), data=self._data[name], api_params=self._api_params)

        resource_mapping = self._api.resource_mapping
        if name in resource_mapping:
            resource = resource_mapping[name]
            api_root = self._api.get_api_root(self._api_params)

            url = api_root.rstrip('/') + '/' + resource['resource'].lstrip('/')
            return TapiocaClient(self._api.__class__(), data=url, api_params=self._api_params,
                                 resource=resource)

    def __getattr__(self, name):
        ret = self._get_client_from_name(name)
        if ret is None:
            raise AttributeError(name)
        return ret

    def __getitem__(self, key):
        ret = self._get_client_from_name(key)
        if ret is None:
            raise KeyError(key)
        return ret

    def __iter__(self):
        return TapiocaClientExecutor(self._api.__class__(),
            data=self._data, request_kwargs=self._request_kwargs, api_params=self._api_params)

    def __dir__(self):
        if self._api and self._data == None:
            return [key for key in self._api.resource_mapping.keys()]

        if isinstance(self._data, dict):
            return self._data.keys()

        return []

    def __str__(self):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        return """<{} object
{}>""".format(self.__class__.__name__, pp.pformat(self._data))

    def _repr_pretty_(self, p, cycle):
        p.text(self.__str__())


class TapiocaClientExecutor(TapiocaClient):

    def __init__(self, api, *args, **kwargs):
        super(TapiocaClientExecutor, self).__init__(api, *args, **kwargs)
        self._iterator_index = 0

    def __call__(self, *args, **kwargs):
        return object.__call__(*args, **kwargs)

    def __getattr__(self, name):
        return object.__getattr__(name)

    def __getitem__(self, key):
        return object.__getitem__(name)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def data(self):
        return self._data

    def response(self):
        if self._response is None:
            raise Exception("This TapiocaClient instance has no response object")
        return self._response

    def _make_request(self, request_method, *args, **kwargs):
        if not 'url' in kwargs:
            kwargs['url'] = self._data

        request_kwargs = self._api.get_request_kwargs(self._api_params, *args, **kwargs)

        response = requests.request(request_method, **request_kwargs)

        try:
            data = self._api.process_response(response)
        except ResponseProcessException as e:
            client = TapiocaClient(self._api.__class__(), data=e.data, response=response,
                request_kwargs=request_kwargs, api_params=self._api_params)
            raise e.tapioca_exception(client=client)

        return TapiocaClient(self._api.__class__(), data=data, response=response,
            request_kwargs=request_kwargs, api_params=self._api_params)

    def get(self, *args, **kwargs):
        return self._make_request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._make_request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._make_request('PUT', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._make_request('PATCH', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._make_request('DELETE', *args, **kwargs)

    def next(self):
        iterator_list = self._api.get_iterator_list(self._data)
        if self._iterator_index >= len(iterator_list):
            new_request_kwargs = self._api.get_iterator_next_request_kwargs(
                self._request_kwargs, self._data, self._response)

            if new_request_kwargs:
                cli = TapiocaClientExecutor(self._api.__class__(), api_params=self._api_params)
                response = cli.get(**new_request_kwargs)
                self._data = response._data
                self._response = response
                self._iterator_index = 0
            else:
                raise StopIteration()

        item = iterator_list[self._iterator_index]
        self._iterator_index += 1

        return TapiocaClient(self._api.__class__(), data=item, api_params=self._api_params)

    def open_docs(self):
        if not self._resource:
            raise KeyError()

        new = 2 # open in new tab
        webbrowser.open(self._resource['docs'], new=new)

    def open_in_browser(self):
        new = 2 # open in new tab
        webbrowser.open(self._data, new=new)
