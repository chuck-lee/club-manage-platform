var financeControllers = angular.module('financeControllers', ['ui.bootstrap']);
financeControllers.controller('transactionController', transactionController);
financeControllers.controller('budgetController', budgetController);
financeControllers.controller('reportController', reportController);
financeControllers.controller('menuController', menuController);

financeControllers.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

function commalizeValue(value) {
    return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function transactionController($scope, $http, $stateParams, year)
{
    $http
    .get('api/v1/transaction/' + year)
    .success(function(data, status, headers, config) {
        $scope.year = year;

        var total = data.previousTotal;
        var transactions = data.transactions;
        transactions.unshift({
            total: commalizeValue(total),
            category: '前期結餘'
        });
        for (var i = 1; i < transactions.length; i++) {
            amount = transactions[i].amount;
            total += amount;
            transactions[i].total = commalizeValue(total);
            transactions[i].income = commalizeValue(amount > 0 ? amount : 0);
            transactions[i].expense = commalizeValue(amount < 0 ? -amount : 0);
        }
        $scope.transactions = transactions;
    })
    .error(function(data, status, headers, config) {
    });
}

function budgetController($scope, $http, $stateParams, $modal, $state, year) {
    $http.get('api/v1/budget/' + year)
    .success(function(data, status, headers, config) {
        var budgets = [];

        var categoryAmount = 0,
            categoryLastReport = 0,
            categoryLastTransaction = 0;
        var typeAmount = 0,
            typeLastReport = 0,
            typeLastTransaction = 0;
        var prevReport = null;
        var currentReport = null;
        while (currentReport = data.budgets.pop()) {
            if (prevReport) {
                if (prevReport.category != currentReport.category) {
                    budgets.unshift({
                        category: prevReport.category,
                        amount: commalizeValue(categoryAmount),
                        last_budget: commalizeValue(categoryLastReport),
                        last_transaction: commalizeValue(categoryLastTransaction)
                    })
                    categoryAmount = 0;
                    categoryLastReport = 0;
                    categoryLastTransaction = 0;
                }

                if (prevReport.type != currentReport.type) {
                    budgets.unshift({
                        type: prevReport.type,
                        amount: commalizeValue(typeAmount),
                        last_budget: commalizeValue(typeLastReport),
                        last_transaction: commalizeValue(typeLastTransaction)
                    })
                    typeAmount = 0;
                    typeLastReport = 0;
                    typeLastTransaction = 0;
                }
            }

            budgets.unshift({
                id: currentReport.id,
                subCategory: currentReport.subCategory,
                amount: commalizeValue(currentReport.amount),
                last_budget: commalizeValue(currentReport.last_budget),
                last_transaction: commalizeValue(currentReport.last_transaction)
            });

            categoryAmount += currentReport.amount;
            categoryLastReport += currentReport.last_budget;
            categoryLastTransaction += currentReport.last_transaction;

            typeAmount += currentReport.amount;
            typeLastReport += currentReport.last_budget;
            typeLastTransaction += currentReport.last_transaction;

            prevReport = currentReport;
        }

        budgets.unshift({
            category: prevReport.category,
            amount: commalizeValue(categoryAmount),
            last_budget: commalizeValue(categoryLastReport),
            last_transaction: commalizeValue(categoryLastTransaction)
        });
        budgets.unshift({
            type: prevReport.type,
            amount: commalizeValue(typeAmount),
            last_budget: commalizeValue(typeLastReport),
            last_transaction: commalizeValue(typeLastTransaction)
        });

        $scope.budgets = budgets;
        $scope.year = year;
    })
    .error(function(data, status, headers, config) {
    });

    $scope.showBudgetDetail = function(budgetId) {
        $modal.open({
            templateUrl: '/static/finance/template/budgetDetail.html',
            controller: ['$scope', '$http', '$modalInstance', 'budgetId',
                function ($scope, $http, $modalInstance, budgetId) {
                    $scope.types = [
                        {
                            value: 1,
                            name: '收入'
                        },
                        {
                            value: -1,
                            name: '支出'
                        }
                    ];

                    $http.get('api/v1/subCategory')
                    .success(function(data, status, headers, config) {
                        $scope.subCategorys = data.subCategorys;

                        $http.get('api/v1/budgetDetail/' + budgetId + '/')
                        .success(function(data, status, headers, config) {
                            $scope.id = data.id;
                            $scope.year = data.year;
                            $scope.budgetType = data.type;
                            $scope.subCategoryId = data.subCategoryId;
                            $scope.amount = data.amount;
                        })
                        .error(function(data, status, headers, config) {
                        });
                    })
                    .error(function(data, status, headers, config) {
                    });


                    $scope.modify = function() {
                        //alert("Modify: " + $scope.id + "/" + $scope.year + "/" + JSON.stringify($scope.budgetType) + "/" + $scope.subCategoryId + "/" + $scope.amount);
                        $http.put('api/v1/budgetDetail/' + $scope.id + '/', {
                            'year': $scope.year,
                            'type': $scope.budgetType,
                            'subCategoryId': $scope.subCategoryId,
                            'amount': $scope.amount
                        })
                        .success(function() {
                            $state.reload();
                            $modalInstance.dismiss($scope.id);
                        })
                        .error(function() {
                            $state.reload();
                            $modalInstance.dismiss($scope.id);
                        });
                    }

                    $scope.delete = function() {
                        $http.delete('api/v1/budgetDetail/' + $scope.id + '/')
                        .success(function() {
                            $state.reload();
                            $modalInstance.dismiss($scope.id);
                        })
                        .error(function() {
                            $state.reload();
                            $modalInstance.dismiss($scope.id);
                        });
                    }

                    $scope.cancel = function() {
                        $modalInstance.dismiss($scope.id);
                    }
            }],
            resolve: {
                budgetId: function() {
                    return budgetId
                }
            }
        });
    };

    $scope.addBudget = function() {
        $modal.open({
            templateUrl: '/static/finance/template/addBudget.html',
            controller: ['$scope', '$http', '$modalInstance',
                function ($scope, $http, $modalInstance) {
                    $scope.types = [
                        {
                            value: 1,
                            name: '收入'
                        },
                        {
                            value: -1,
                            name: '支出'
                        }
                    ];

                    $http.get('api/v1/subCategory')
                    .success(function(data, status, headers, config) {
                        $scope.subCategorys = data.subCategorys;
                        $scope.year = year;
                        //$scope.budgetType = 1;
                        //$scope.subCategoryId = data.subCategoryId;
                        $scope.amount = 0;
                    })
                    .error(function(data, status, headers, config) {
                    });

                    $scope.add = function() {
                        //alert("Modify: " + $scope.id + "/" + $scope.year + "/" + JSON.stringify($scope.budgetType) + "/" + $scope.subCategoryId + "/" + $scope.amount);
                        $http.post('api/v1/budgetDetail/0/', {
                            'year': $scope.year,
                            'type': $scope.budgetType,
                            'subCategoryId': $scope.subCategoryId,
                            'amount': $scope.amount
                        })
                        .success(function() {
                            $state.reload();
                            $modalInstance.dismiss($scope.id);
                        })
                        .error(function() {
                            $state.reload();
                            $modalInstance.dismiss($scope.id);
                        });
                    }

                    $scope.cancel = function() {
                        $modalInstance.dismiss();
                    }
            }]
        });
    };
}

function reportController($scope, $http, $stateParams, year) {
    $http.get('api/v1/report/' + year)
    .success(function(data, status, headers, config) {
        var reports = [];

        var categoryBudget = 0,
            categoryTransaction = 0;
        var typeBudget = 0,
            typeTransaction = 0;
        var prevReport = null;
        var currentReport = null;
        while (currentReport = data.reports.pop()) {
            if (prevReport) {
                if (prevReport.category != currentReport.category) {
                    reports.unshift({
                        category: prevReport.category,
                        budget: commalizeValue(categoryBudget),
                        transaction: commalizeValue(categoryTransaction)
                    })
                    categoryBudget = 0;
                    categoryTransaction = 0;
                }

                if (prevReport.type != currentReport.type) {
                    reports.unshift({
                        type: prevReport.type,
                        budget: commalizeValue(typeBudget),
                        transaction: commalizeValue(typeTransaction)
                    })
                    typeBudget = 0;
                    typeTransaction = 0;
                }
            }

            reports.unshift({
                subCategory: currentReport.subCategory,
                budget: commalizeValue(currentReport.budget),
                transaction: commalizeValue(currentReport.transaction)
            });

            categoryBudget += currentReport.budget;
            categoryTransaction += currentReport.transaction;

            typeBudget += currentReport.budget;
            typeTransaction += currentReport.transaction;

            prevReport = currentReport;
        }

        reports.unshift({
            category: prevReport.category,
            budget: commalizeValue(categoryBudget),
            transaction: commalizeValue(categoryTransaction)
        });
        reports.unshift({
            type: prevReport.type,
            budget: commalizeValue(typeBudget),
            transaction: commalizeValue(typeTransaction)
        });

        $scope.reports = reports;
        $scope.year = year;
    })
    .error(function(data, status, headers, config) {
    });
}

function menuController($scope, $http, $stateParams) {
    $http.get('api/v1/availableYears')
    .success(function(data, status, headers, config) {
        $scope.availableYears = data.availableYears;
        $scope.selectedYear = $stateParams.year
    })
    .error(function(data, status, headers, config) {
    });
}
