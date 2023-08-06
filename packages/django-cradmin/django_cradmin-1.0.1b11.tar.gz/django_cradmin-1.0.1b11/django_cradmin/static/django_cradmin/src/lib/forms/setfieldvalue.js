(function() {
  var app;

  app = angular.module('djangoCradmin.forms.setfieldvalue', ['cfp.hotkeys']);

  /**
  Directive for setting the value of a form field to specified value.
  
  Example:
  
  ```
    <button type="button"
            django-cradmin-setfieldvalue="2015-12-24 12:30"
            django-cradmin-setfieldvalue-field-id="my_datetimefield_id">
        Set value to 2015-12-24 12:30
    </button>
  ```
  */


  app.directive('djangoCradminSetfieldvalue', [
    function() {
      return {
        scope: {
          value: "@djangoCradminSetfieldvalue",
          fieldid: "@djangoCradminSetfieldvalueFieldId"
        },
        link: function($scope, $element) {
          var fieldElement;
          fieldElement = angular.element("#" + $scope.fieldid);
          if (fieldElement.length === 0) {
            return typeof console !== "undefined" && console !== null ? typeof console.error === "function" ? console.error("Could not find a field with the '" + $scope.fieldid + "' ID.") : void 0 : void 0;
          } else {
            $element.on('click', function() {
              fieldElement.val($scope.value);
              return fieldElement.trigger('change');
            });
          }
        }
      };
    }
  ]);

}).call(this);
