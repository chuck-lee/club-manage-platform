var financeControllers = angular.module('financeControllers', ['ui.bootstrap']);
financeControllers.controller('transactionController', transactionController);
financeControllers.controller('budgetController', budgetController);
financeControllers.controller('reportController', reportController);
financeControllers.controller('menuController', menuController);
financeControllers.controller('categoryController', categoryController);

financeControllers.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

function transactionController($scope, $http, $stateParams, $modal, $state, year)
{
    originData = {
        total: 0,
        transactions: []
    };

    function getMonthFromDate(date) {
        return parseInt(date.split('-')[1], 10);
    }

    function updateTransactionList() {
        var previousAmount = originData.total;
        var originalTransactions = originData.transactions;

        var transactions = [];
        var i = 0;
        for (i = 0;
             i < originalTransactions.length &&
             getMonthFromDate(originalTransactions[i].date) < $scope.monthStart;
             i++) {
                previousAmount += originalTransactions[i].amount;
        }

        var total = previousAmount;
        for (; i < originalTransactions.length &&
             getMonthFromDate(originalTransactions[i].date) <= $scope.monthEnd;
             i++) {
                var transaction = originalTransactions[i];
                var amount = transaction.amount;

                total += amount;
                transaction.total = total;
                transaction.income = amount > 0 ? amount : 0;
                transaction.expense = amount < 0 ? -amount : 0;

                transactions.push(transaction);
        }

        $scope.previousAmount = previousAmount;
        $scope.transactions = transactions;
    }

    $scope.$watch("monthStart", function(newValue, oldValue) {
        if (newValue > $scope.monthEnd) {
            $scope.monthEnd = newValue;
        }

        updateTransactionList();
    });

    $scope.$watch("monthEnd", function(newValue, oldValue) {
        if (newValue < $scope.monthStart) {
            $scope.monthStart = newValue;
        }

        updateTransactionList();
    });

    $http
    .get('api/v1/transaction/' + year)
    .success(function(data, status, headers, config) {
        originData.total = data.previousTotal;
        originData.transactions = data.transactions;

        $scope.year = year;
        $scope.monthStart = 1;
        $scope.monthEnd = 12;
        updateTransactionList();
    })
    .error(function(data, status, headers, config) {
    });

    $scope.showTransactionDetail = function(transactionId) {
        $modal.open({
            templateUrl: '/static/finance/template/transactionDetail.html',
            controller: ['$scope', '$http', '$modalInstance', 'transactionId',
                function ($scope, $http, $modalInstance, transactionId) {
                    $scope.$watch("date", function(newDate, oldDate) {
                        if (!newDate) {
                            return;
                        }
                        newDate = newDate.split('-');
                        newYear = new Date(parseInt(newDate[0], 10),
                                           parseInt(newDate[1], 10) - 1,
                                           parseInt(newDate[2])).getFullYear();
                        oldYear = 0;
                        if (oldDate) {
                            oldDate = oldDate.split('-');
                            oldYear = new Date(parseInt(oldDate[0], 10),
                                               parseInt(oldDate[1], 10) - 1,
                                               parseInt(oldDate[2])).getFullYear();
                        }

                        if (newYear && newYear != oldYear) {
                            $http.get('api/v1/budget/' + newYear)
                            .success(function(data, status, headers, config) {
                                $scope.budgets = data.budgets;
                            })
                            .error(function(data, status, headers, config) {
                            });
                        }
                    });

                    $http.get('api/v1/payees')
                    .success(function(data, status, headers, config) {
                        $scope.payees = data.payees;

                        $http.get('api/v1/transactionDetail/' + transactionId + '/')
                        .success(function(data, status, headers, config) {
                            $scope.id = data.id;
                            $scope.date = data.date;
                            $scope.serial = data.serial;
                            $scope.payeeId = data.payeeId;
                            $scope.amount = data.amount;
                            $scope.comment = data.comment;
                            budgetId = data.budgetId;

                            $http.get('api/v1/budget/' + $scope.date.split('-')[0])
                            .success(function(data, status, headers, config) {
                                $scope.budgets = data.budgets;
                                $scope.budgetId = budgetId;
                            })
                            .error(function(data, status, headers, config) {
                            });
                        })
                        .error(function(data, status, headers, config) {
                        });
                    })
                    .error(function(data, status, headers, config) {
                    });

                    $scope.modify = function() {
                        $http.put('api/v1/transactionDetail/' + transactionId + '/', {
                            'date': $scope.date,
                            'serial': $scope.serial,
                            'budgetId': $scope.budgetId,
                            'payeeId': $scope.payeeId,
                            'amount': $scope.amount,
                            'comment': $scope.comment
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
                        $http.delete('api/v1/transactionDetail/' + transactionId + '/')
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
                transactionId: function() {
                    return transactionId;
                }
            }
        });
    }

    $scope.addTransaction = function() {
        $modal.open({
            templateUrl: '/static/finance/template/addTransaction.html',
            controller: ['$scope', '$http', '$modalInstance',
                function ($scope, $http, $modalInstance) {
                    $scope.$watch("date", function(newDate, oldDate) {
                        if (!newDate) {
                            return;
                        }
                        newDate = newDate.split('-');
                        newYear = new Date(parseInt(newDate[0], 10),
                                           parseInt(newDate[1], 10) - 1,
                                           parseInt(newDate[2])).getFullYear();
                        oldYear = 0;
                        if (oldDate) {
                            oldDate = oldDate.split('-');
                            oldYear = new Date(parseInt(oldDate[0], 10),
                                               parseInt(oldDate[1], 10) - 1,
                                               parseInt(oldDate[2])).getFullYear();
                        }

                        if (newYear && newYear != oldYear) {
                            $http.get('api/v1/budget/' + newYear)
                            .success(function(data, status, headers, config) {
                                $scope.budgets = data.budgets;
                            })
                            .error(function(data, status, headers, config) {
                            });
                        }
                    });

                    today = new Date;
                    $scope.amount = 0
                    $scope.date = year + "-" +
                                  (today.getMonth() + 1) + "-" +
                                  today.getDate();

                    $http.get('api/v1/budget/' + year)
                    .success(function(data, status, headers, config) {
                        $scope.budgets = data.budgets;

                        $http.get('api/v1/payees')
                        .success(function(data, status, headers, config) {
                            $scope.payees = data.payees;
                        })
                        .error(function(data, status, headers, config) {
                        });
                    })
                    .error(function(data, status, headers, config) {
                    });

                    $scope.add = function() {
                        $http.post('api/v1/transactionDetail/0/', {
                            'date': $scope.date,
                            'serial': $scope.serial,
                            'budgetId': $scope.budgetId,
                            'payeeId': $scope.payeeId,
                            'amount': $scope.amount,
                            'comment': $scope.comment
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
        var prevBudget = null;
        var currentBudget = null;
        while (currentBudget = data.budgets.pop()) {
            if (prevBudget) {
                if (prevBudget.categoryId != currentBudget.categoryId) {
                    budgets.unshift({
                        category: prevBudget.categoryName,
                        amount: categoryAmount,
                        last_budget: categoryLastReport,
                        last_transaction: categoryLastTransaction
                    })
                    categoryAmount = 0;
                    categoryLastReport = 0;
                    categoryLastTransaction = 0;
                }

                if (prevBudget.type != currentBudget.type) {
                    budgets.unshift({
                        type: prevBudget.type,
                        amount: typeAmount,
                        last_budget: typeLastReport,
                        last_transaction: typeLastTransaction
                    })
                    typeAmount = 0;
                    typeLastReport = 0;
                    typeLastTransaction = 0;
                }
            }

            budgets.unshift({
                id: currentBudget.id,
                subCategory: currentBudget.subCategoryName,
                amount: currentBudget.amount,
                last_budget: currentBudget.last_budget,
                last_transaction: currentBudget.last_transaction
            });

            categoryAmount += currentBudget.amount;
            categoryLastReport += currentBudget.last_budget;
            categoryLastTransaction += currentBudget.last_transaction;

            typeAmount += currentBudget.amount;
            typeLastReport += currentBudget.last_budget;
            typeLastTransaction += currentBudget.last_transaction;

            prevBudget = currentBudget;
        }

        if (prevBudget) {
            budgets.unshift({
                category: prevBudget.categoryName,
                amount: categoryAmount,
                last_budget: categoryLastReport,
                last_transaction: categoryLastTransaction
            });
            budgets.unshift({
                type: prevBudget.type,
                amount: typeAmount,
                last_budget: typeLastReport,
                last_transaction: typeLastTransaction
            });
        }

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
                        $http.put('api/v1/budgetDetail/' + budgetId + '/', {
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
                        $http.delete('api/v1/budgetDetail/' + budgetId + '/')
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
                    return budgetId;
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

function reportController($scope, $http, $stateParams, $modal, $state, year) {
    function reportObject(type, category, subCategory, budget, current, last) {
        var total = current + last;
        return {
            type: type,
            category: category,
            subCategory:subCategory,
            budget: budget,
            current: current,
            last: last,
            total: total,
            remain: budget - total,
            exeRate: budget ? total / budget : 0
        };
    }

    $scope.month = 0;

    $scope.$watch("month", function(newMonth, oldMonth) {
        var url = 'api/v1/report/' + year;
        if ($scope.month != 0) {
            url += '/' + $scope.month;
        }

        $http.get(url)
        .success(function(data, status, headers, config) {
            var reports = [];

            var categoryBudget = 0,
                categoryCurrent = 0,
                categoryLast = 0;
            var typeBudget = 0,
                typeCurrent = 0,
                typeLast = 0;
            var prevReport = null;
            var currentReport = null;
            var summary = {
                income: 0,
                expense: 0,
                lastBalance: data.lastBalance,
            };
            while (currentReport = data.reports.pop()) {
                if (prevReport) {
                    if (prevReport.category != currentReport.category) {
                        reports.unshift(
                            reportObject('', prevReport.category, '',
                                         categoryBudget, categoryCurrent, categoryLast)
                        )
                        categoryBudget = 0;
                        categoryCurrent = 0;
                        categoryLast = 0
                    }

                    if (prevReport.type != currentReport.type) {
                        reports.unshift(
                            reportObject(prevReport.type, '', '',
                                         typeBudget, typeCurrent, typeLast)
                        )
                        summary.expense = typeCurrent; // Ugly but based on API's behavior
                        typeBudget = 0;
                        typeCurrent = 0;
                        typeLast = 0;
                    }
                }

                reports.unshift(
                    reportObject('', '', currentReport.subCategory,
                                 currentReport.budget, currentReport.current, currentReport.last)
                );

                categoryBudget += currentReport.budget;
                categoryCurrent += currentReport.current;
                categoryLast += currentReport.last;

                typeBudget += currentReport.budget;
                typeCurrent += currentReport.current;
                typeLast += currentReport.last;

                prevReport = currentReport;
            }

            if (prevReport) {
                reports.unshift(
                    reportObject('', prevReport.category, '',
                                 categoryBudget, categoryCurrent, categoryLast)
                );
                reports.unshift(
                    reportObject(prevReport.type, '', '',
                                 typeBudget, typeCurrent, typeLast)
                );
                summary.income = typeCurrent; // Ugly but based on API's behavior
            }

            $scope.reports = reports;
            $scope.year = year;
            $scope.summary = summary;
        })
        .error(function(data, status, headers, config) {
        });
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

function categoryController($scope, $http, $stateParams, $modal, $state) {
    $http.get('api/v1/category')
    .success(function(data, status, headers, config) {
        $scope.categorys = data.categorys;
        for (var i = 0; i < $scope.categorys.length; i++) {
            $scope.categorys[i].type = 'category';
        }

        $http.get('api/v1/subCategory')
        .success(function(data, status, headers, config) {
            var subCategory = null;
            while (subCategory = data.subCategorys.pop()) {
                for (var i = 0; i < $scope.categorys.length; i++) {
                    if ($scope.categorys[i].type == 'category' &&
                        $scope.categorys[i].id == subCategory.categoryId) {
                        $scope.categorys.splice(i + 1, 0, {
                            "id": subCategory.id,
                            "name": subCategory.name
                        });
                    }
                }
            }
        })
        .error(function(data, status, headers, config) {
        });
    })
    .error(function(data, status, headers, config) {
    });

    $scope.addCategory = function() {
        $modal.open({
            templateUrl: '/static/finance/template/addCategory.html',
            controller: ['$scope', '$http', '$modalInstance',
                function ($scope, $http, $modalInstance) {
                    $scope.add = function() {
                        $http.post('api/v1/categoryDetail/0/', {
                            'name': $scope.name,
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

    $scope.addSubCategory = function() {
        $modal.open({
            templateUrl: '/static/finance/template/addSubCategory.html',
            controller: ['$scope', '$http', '$modalInstance',
                function ($scope, $http, $modalInstance) {
                    $http.get('api/v1/category')
                    .success(function(data, status, headers, config) {
                        $scope.categorys = data.categorys;
                    })
                    .error(function(data, status, headers, config) {
                    });

                    $scope.add = function() {
                        $http.post('api/v1/subCategoryDetail/0/', {
                            'categoryId': $scope.categoryId,
                            'name': $scope.name,
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

    $scope.showCategoryDetail = function(categoryId) {
        $modal.open({
            templateUrl: '/static/finance/template/categoryDetail.html',
            controller: ['$scope', '$http', '$modalInstance', 'categoryId',
                function ($scope, $http, $modalInstance, categoryId) {
                    $http.get('api/v1/categoryDetail/' + categoryId + '/')
                    .success(function(data, status, headers, config) {
                        $scope.name = data.name;
                    })
                    .error(function(data, status, headers, config) {
                    });;

                    $scope.modify = function() {
                        $http.put('api/v1/categoryDetail/' + categoryId + '/', {
                            'name': $scope.name
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
                        $http.delete('api/v1/categoryDetail/' + categoryId + '/')
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
                categoryId: function() {
                    return categoryId;
                }
            }
        });
    };

    $scope.showSubCategoryDetail = function(subCategoryId) {
        $modal.open({
            templateUrl: '/static/finance/template/subCategoryDetail.html',
            controller: ['$scope', '$http', '$modalInstance', 'subCategoryId',
                function ($scope, $http, $modalInstance, subCategoryId) {
                    $http.get('api/v1/category')
                    .success(function(data, status, headers, config) {
                        $scope.categorys = data.categorys;

                        $http.get('api/v1/subCategoryDetail/' + subCategoryId + '/')
                        .success(function(data, status, headers, config) {
                            $scope.categoryId = data.categoryId;
                            $scope.name = data.name;
                        })
                        .error(function(data, status, headers, config) {
                        });;
                    })
                    .error(function(data, status, headers, config) {
                    });

                    $scope.modify = function() {
                        $http.put('api/v1/subCategoryDetail/' + subCategoryId + '/', {
                            'categoryId': $scope.categoryId,
                            'name': $scope.name
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
                        $http.delete('api/v1/subCategoryDetail/' + subCategoryId + '/')
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
                subCategoryId: function() {
                    return subCategoryId;
                }
            }
        });
    };
}
