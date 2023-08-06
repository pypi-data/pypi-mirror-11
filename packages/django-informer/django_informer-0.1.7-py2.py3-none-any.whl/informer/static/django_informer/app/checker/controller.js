(function () {
    'use strict';

    var checker = angular.module('informer.checker', ['ngResource']);

    checker.controller('DetailController', ['$scope', '$routeParams', 'InformerService', DetailController]);

    function DetailController ($scope, params, Informer) {
        $scope.informer = {};

        Informer.get({ 'informer': params.informer }, successOnGetInformerDetails, fail);

        function successOnGetInformerDetails (response) {
            $scope.informer = response;
        }

        function fail () {
            $scope.informer = {};
            $scope.message = 'Crap. A error ocurred.';
        }
    }
})();
