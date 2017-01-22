var myApp = angular.module('dwApp', [])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });

myApp.controller('DataController', function($scope, $http){

	$scope.header = 'Hello datawiz.io!';

	var getDWdata = function(){
		$http.get("data").then(function(response){
				// console.log(response.data);
				console.log('pisun!');
	      var dwData = response.data;
	      $scope.dwData = dwData;
	      }, function(error){}
	    );
	};
	getDWdata();
});