var financeApp = angular.module('financeApp', [
    'ui.router',
    'financeControllers'
]);

financeApp.config(['$stateProvider', '$urlRouterProvider',
    function($stateProvider, $urlRouterProvider) {
        $urlRouterProvider
            .when('/:year/', '/:year/budget')
            .otherwise('/' + (new Date().getFullYear()) + '/budget');

        $stateProvider
            .state('year', {
                abstract: true,
                url: '/{year:int}',
                views: {
                    "menuView": {
                        templateUrl: '/static/finance/template/menu.html',
                        controller: 'menuController'
                    },
                    "dataView": {
                        template: '<div class="dataView" ui-view="dataView"></div>'
                    }
                },
                resolve: {
                    year: ['$stateParams', function($stateParams){
                        return $stateParams.year;
                    }]
                }
            })
            .state('year.budget',{
                url: '/budget',
                views: {
                    "dataView": {
                        templateUrl: '/static/finance/template/budget.html',
                        controller: 'budgetController'
                    }
                }
            })
            .state('year.transaction',{
                url: '/transaction',
                views: {
                    "dataView": {
                        templateUrl: '/static/finance/template/transaction.html',
                        controller: 'transactionController'
                    }
                }
            })
            .state('year.report',{
                url: '/report',
                views: {
                    "dataView": {
                        templateUrl: '/static/finance/template/report.html',
                        controller: 'reportController'
                    }
                }
            })
            .state('category', {
                url: '/category',
                views: {
                    "menuView": {
                        templateUrl: '/static/finance/template/menu.html',
                        controller: 'menuController'
                    },
                    "dataView": {
                        templateUrl: '/static/finance/template/category.html',
                        controller: 'categoryController'
                    }
                }
            })
    }
]);
