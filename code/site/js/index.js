angular
  .module('MyApp',['ngMaterial', 'ngMessages', 'material.svgAssetsCache'])
  .controller('DemoCtrl', function($scope, $http, $element, $window) {
    $scope.report = {
      query: '',//'SSE Crash in PARTs During SAM Integration',
      // description: ''//"On 2/4/2008 in ATLO AR618 while integrating SAM into PARTs,  the following problem was observed:\n\n"+
      // "The SSE crashed twice during SAM integration.​ Both times we were running SAM's baseline functional test script.​ The first time,  the SSE crashed at 19:11:01,  6:46 minutes into the SAM script.​ The second time,  the SSE crashed at 21:05:22,  5:21 minutes into the SAM script.​ In both cases we continued executing the SAM functional test and then powered off SAM,  the flight system,  and the SSE.​\n\n"+
      // "It is rather unlikely that the SAM test had anything to do with the SSE crash.​ Garett Sohl investigated the issue both times and potentially has more information he picked up from the logs.​"
    };

    $scope.SearchResults = function() {
      parameter = JSON.stringify({
        AnalysisImpacts: $scope.AnalysisImpacts || "",
        CorrectiveAction:$scope.CorrectiveAction || "",
        Description:$scope.Description || "",
        ExecutiveSummary:$scope.ExecutiveSummary || "",
        Issues:$scope.Issues || "",
        TestVerification:$scope.TestVerification || "",
        Title:$scope.Title || "",
        WorkstationName:$scope.WorkstationName || "",
        Anomaly_ID:$scope.Anomaly_ID || "",
      })

      $http({method : 'POST',url : "http://127.0.0.1:5000/PRS/api/v1.0/search", data:parameter})
          .success(function(data, status) {
            console.log(data);
              $scope.search_results = data.search_results;
              $scope.AnalysisImpacts = data.form.AnalysisImpacts || "";
              $scope.CorrectiveAction = data.form.CorrectiveAction || "";
              $scope.Description = data.form.Description || "";
              $scope.ExecutiveSummary = data.form.ExecutiveSummary || "";
              $scope.Issues = data.form.Issues || "";
              $scope.TestVerification = data.form.TestVerification || "";
              $scope.Title = data.form.Title || "";
              $scope.WorkstationName = data.form.WorkstationName || "";
              console.log(data);
              console.log('worked');
              console.log($element[0]);
          })
          .error(function(data, status) {
              console.log("Error");
          });
    };

  })
  .config(function($mdThemingProvider) {

    // Configure a dark theme with primary foreground yellow

    $mdThemingProvider.theme('docs-dark', 'default')
      .primaryPalette('yellow')
      .dark();

  });


/**
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that can be foundin the LICENSE file at http://material.angularjs.org/HEAD/license.
**/
