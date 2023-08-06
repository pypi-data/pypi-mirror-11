(function () {
    'use strict';

    var checker = angular.module('informer.checker');

    checker.factory('InformerDiscoverService', ['$resource', 'CONFIGURATION', InformerDiscoverService]);
    checker.factory('InformerService', ['$resource', 'CONFIGURATION', InformerService]);

    function InformerDiscoverService ($resource, Configuration) {
        return $resource(
            Configuration.URL + 'discover/',
            {},
            {
                'query': { method: 'GET' }
            }
        );
    }

    function InformerService ($resource, Configuration) {
        return $resource(
            Configuration.URL + ':informer/',
            {'informer': '@informer'},
            {
                'get': { method: 'GET' }
            }
        );
    }

})();
