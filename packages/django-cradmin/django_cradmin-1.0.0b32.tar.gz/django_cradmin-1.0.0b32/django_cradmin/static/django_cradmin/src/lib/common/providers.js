(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  angular.module('djangoCradmin.providers', []).provider('djangoCradminWindowDimensions', function() {
    /** Provider that makes it easy to listen for window resize.
    
    How it works
    ============
    You register a ``scope`` with the provider. Each time the window
    is resized, the provider will call ``scope.onWindowResize()``.
    The provider uses a ``300ms`` timeout before it triggers a
    resize, so your ``onWindowResize`` method will not be flooded
    with every pixel change.
    
    Example
    =======
    
    ```coffeescript
    mymodule.directive('myDirective', [
      'djangoCradminWindowDimensions'
      (djangoCradminWindowDimensions) ->
        return {
          controller: ($scope) ->
            $scope.onWindowResize = (newWindowDimensions) ->
              console.log 'Window was resized to', newWindowDimensions
            return
    
          link: ($scope, element, attrs) ->
            djangoCradminWindowDimensions.register $scope
            $scope.$on '$destroy', ->
              djangoCradminWindowDimensions.unregister $scope
            return
        }
    ])
    ```
    */

    var WindowDimensionsProvider;
    WindowDimensionsProvider = (function() {
      function WindowDimensionsProvider($window, timeout) {
        this.timeout = timeout;
        this._onWindowResize = __bind(this._onWindowResize, this);
        this.mainWindow = angular.element($window);
        this.windowDimensions = this._getWindowDimensions();
        this.applyResizeTimer = null;
        this.applyResizeTimerTimeoutMs = 300;
        this.listeningScopes = [];
      }

      WindowDimensionsProvider.prototype.register = function(scope) {
        var scopeIndex;
        scopeIndex = this.listeningScopes.indexOf(scope);
        if (scopeIndex !== -1) {
          console.error('Trying to register a scope that is already registered with ' + 'djangoCradminWindowDimensions. Scope:', scope);
          return;
        }
        if (this.listeningScopes.length < 1) {
          this.mainWindow.bind('resize', this._onWindowResize);
        }
        this.listeningScopes.push(scope);
        return scope.onWindowResize(this.windowDimensions);
      };

      WindowDimensionsProvider.prototype.unregister = function(scope) {
        var scopeIndex;
        scopeIndex = this.listeningScopes.indexOf(scope);
        if (scopeIndex === -1) {
          console.error('Trying to unregister a scope that is not registered with ' + 'djangoCradminWindowDimensions. Scope:', scope);
        }
        this.listeningScopes.splice(scopeIndex, 1);
        if (this.listeningScopes.length < 1) {
          return this.mainWindow.unbind('resize', this._onWindowResize);
        }
      };

      WindowDimensionsProvider.prototype._getWindowDimensions = function() {
        return {
          height: this.mainWindow.height(),
          width: this.mainWindow.width()
        };
      };

      WindowDimensionsProvider.prototype._setWindowDimensions = function() {
        var newWindowDimensions;
        newWindowDimensions = this._getWindowDimensions();
        if (!angular.equals(newWindowDimensions, this.windowDimensions)) {
          this.windowDimensions = newWindowDimensions;
          return this._onWindowDimensionsChange();
        }
      };

      WindowDimensionsProvider.prototype._onWindowDimensionsChange = function() {
        var scope, _i, _len, _ref, _results;
        _ref = this.listeningScopes;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          scope = _ref[_i];
          _results.push(scope.onWindowResize(this.windowDimensions));
        }
        return _results;
      };

      WindowDimensionsProvider.prototype._onWindowResize = function() {
        var _this = this;
        this.timeout.cancel(this.applyResizeTimer);
        return this.applyResizeTimer = this.timeout(function() {
          return _this._setWindowDimensions();
        }, this.applyResizeTimerTimeoutMs);
      };

      return WindowDimensionsProvider;

    })();
    this.$get = [
      '$window', '$timeout', function($window, $timeout) {
        return new WindowDimensionsProvider($window, $timeout);
      }
    ];
    return this;
  });

}).call(this);
