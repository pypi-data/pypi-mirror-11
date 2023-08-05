(function() {
  var app;

  app = angular.module('djangoCradmin.forms.datetimewidget', ['ui.bootstrap']);

  app.controller('CradminDateFieldController', function($scope, $filter) {
    $scope.init = function() {
      $scope.datepicker_is_open = false;
    };
    $scope.open_datepicker = function($event) {
      $event.preventDefault();
      $event.stopPropagation();
      $scope.datepicker_is_open = true;
    };
    $scope.set_date_from_string = function(datestr) {
      if (datestr) {
        $scope.datevalue = new Date(datestr);
        $scope.datefield_changed();
      }
    };
    $scope.datefield_changed = function() {
      var datestr;
      datestr = $filter('date')($scope.datevalue, 'yyyy-MM-dd');
      $scope.hiddendatefieldvalue = datestr;
    };
    $scope.init();
  });

  app.controller('CradminTimeFieldController', function($scope, $filter) {
    $scope.set_time_from_string = function(timestr) {
      if (timestr) {
        $scope.timevalue = new Date(timestr);
      } else {
        $scope.timevalue = new Date();
      }
      $scope.timefield_changed();
    };
    return $scope.timefield_changed = function() {
      var timestr;
      timestr = $filter('date')($scope.timevalue, 'HH:mm');
      $scope.hiddentimefieldvalue = timestr;
    };
  });

}).call(this);
