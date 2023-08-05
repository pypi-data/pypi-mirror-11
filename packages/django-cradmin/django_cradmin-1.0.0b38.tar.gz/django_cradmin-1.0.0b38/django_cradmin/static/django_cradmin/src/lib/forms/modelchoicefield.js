(function() {
  angular.module('djangoCradmin.forms.modelchoicefield', []).provider('djangoCradminModelChoiceFieldCoordinator', function() {
    var ModelChoiceFieldOverlay;
    ModelChoiceFieldOverlay = (function() {
      function ModelChoiceFieldOverlay() {
        this.modelChoiceFieldIframeWrapper = null;
        this.bodyContentWrapperElement = angular.element('#django_cradmin_bodycontentwrapper');
        this.bodyElement = angular.element('body');
      }

      ModelChoiceFieldOverlay.prototype.registerModeChoiceFieldIframeWrapper = function(modelChoiceFieldIframeWrapper) {
        return this.modelChoiceFieldIframeWrapper = modelChoiceFieldIframeWrapper;
      };

      ModelChoiceFieldOverlay.prototype.onChangeValueBegin = function(fieldWrapperScope) {
        return this.modelChoiceFieldIframeWrapper.onChangeValueBegin(fieldWrapperScope);
      };

      ModelChoiceFieldOverlay.prototype.addBodyContentWrapperClass = function(cssclass) {
        return this.bodyContentWrapperElement.addClass(cssclass);
      };

      ModelChoiceFieldOverlay.prototype.removeBodyContentWrapperClass = function(cssclass) {
        return this.bodyContentWrapperElement.removeClass(cssclass);
      };

      ModelChoiceFieldOverlay.prototype.disableBodyScrolling = function() {
        return this.bodyElement.addClass('django-cradmin-noscroll');
      };

      ModelChoiceFieldOverlay.prototype.enableBodyScrolling = function() {
        return this.bodyElement.removeClass('django-cradmin-noscroll');
      };

      return ModelChoiceFieldOverlay;

    })();
    this.$get = function() {
      return new ModelChoiceFieldOverlay();
    };
    return this;
  }).directive('djangoCradminModelChoiceFieldIframeWrapper', [
    '$window', '$timeout', 'djangoCradminModelChoiceFieldCoordinator', function($window, $timeout, djangoCradminModelChoiceFieldCoordinator) {
      return {
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.origin = "" + window.location.protocol + "//" + window.location.host;
          $scope.mainWindow = angular.element($window);
          $scope.bodyElement = angular.element($window.document.body);
          $scope.windowDimensions = null;
          djangoCradminModelChoiceFieldCoordinator.registerModeChoiceFieldIframeWrapper(this);
          this.setIframe = function(iframeScope) {
            return $scope.iframeScope = iframeScope;
          };
          this._setField = function(fieldScope) {
            return $scope.fieldScope = fieldScope;
          };
          this._setPreviewElement = function(previewElementScope) {
            return $scope.previewElementScope = previewElementScope;
          };
          this.setLoadSpinner = function(loadSpinnerScope) {
            return $scope.loadSpinnerScope = loadSpinnerScope;
          };
          this.setIframeWrapperInner = function(iframeInnerScope) {
            return $scope.iframeInnerScope = iframeInnerScope;
          };
          this.onChangeValueBegin = function(fieldWrapperScope) {
            this._setField(fieldWrapperScope.fieldScope);
            this._setPreviewElement(fieldWrapperScope.previewElementScope);
            djangoCradminModelChoiceFieldCoordinator.addBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper');
            $scope.iframeScope.beforeShowingIframe(fieldWrapperScope.iframeSrc);
            $scope.mainWindow.bind('resize', $scope.onWindowResize);
            return $scope.show();
          };
          this.onIframeLoadBegin = function() {
            return $scope.loadSpinnerScope.show();
          };
          this.onIframeLoaded = function() {
            $scope.iframeInnerScope.show();
            return $scope.loadSpinnerScope.hide();
          };
          $scope.onChangeValue = function(event) {
            var data;
            if (event.origin !== $scope.origin) {
              console.error("Message origin '" + event.origin + "' does not match current origin '" + $scope.origin + "'.");
              return;
            }
            data = angular.fromJson(event.data);
            if ($scope.fieldScope.fieldid !== data.fieldid) {
              return;
            }
            $scope.fieldScope.setValue(data.value);
            $scope.previewElementScope.setPreviewHtml(data.preview);
            $scope.mainWindow.unbind('resize', $scope.onWindowResize);
            djangoCradminModelChoiceFieldCoordinator.removeBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper');
            $scope.hide();
            return $scope.iframeScope.afterFieldValueChange();
          };
          $window.addEventListener('message', $scope.onChangeValue, false);
          $scope.getWindowDimensions = function() {
            return {
              height: $scope.mainWindow.height(),
              width: $scope.mainWindow.width()
            };
          };
          $scope.$watch('windowDimensions', (function(newSize, oldSize) {
            $scope.iframeScope.setIframeSize();
          }), true);
          $scope.onWindowResize = function() {
            $timeout.cancel($scope.applyResizeTimer);
            $scope.applyResizeTimer = $timeout(function() {
              $scope.windowDimensions = $scope.getWindowDimensions();
              return $scope.$apply();
            }, 300);
          };
          $scope.show = function() {
            $scope.iframeWrapperElement.addClass('django-cradmin-floating-fullsize-iframe-wrapper-show');
            djangoCradminModelChoiceFieldCoordinator.disableBodyScrolling();
            return djangoCradminModelChoiceFieldCoordinator.addBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper-push');
          };
          $scope.hide = function() {
            $scope.iframeWrapperElement.removeClass('django-cradmin-floating-fullsize-iframe-wrapper-show');
            djangoCradminModelChoiceFieldCoordinator.enableBodyScrolling();
            return djangoCradminModelChoiceFieldCoordinator.removeBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper-push');
          };
          this.closeIframe = function() {
            return $scope.hide();
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.iframeWrapperElement = element;
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldIframeWrapperInner', [
    '$window', function($window) {
      return {
        require: '^^djangoCradminModelChoiceFieldIframeWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.scrollToTop = function() {
            return $scope.element.scrollTop(0);
          };
          $scope.show = function() {
            return $scope.element.removeClass('ng-hide');
          };
          $scope.hide = function() {
            return $scope.element.addClass('ng-hide');
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.element = element;
          wrapperCtrl.setIframeWrapperInner(scope);
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldIframeClosebutton', function() {
    return {
      require: '^djangoCradminModelChoiceFieldIframeWrapper',
      restrict: 'A',
      scope: {},
      link: function(scope, element, attrs, iframeWrapperCtrl) {
        element.on('click', function(e) {
          e.preventDefault();
          return iframeWrapperCtrl.closeIframe();
        });
      }
    };
  }).directive('djangoCradminModelChoiceFieldLoadSpinner', function() {
    return {
      require: '^^djangoCradminModelChoiceFieldIframeWrapper',
      restrict: 'A',
      scope: {},
      controller: function($scope) {
        $scope.hide = function() {
          return $scope.element.addClass('ng-hide');
        };
        return $scope.show = function() {
          return $scope.element.removeClass('ng-hide');
        };
      },
      link: function(scope, element, attrs, wrapperCtrl) {
        scope.element = element;
        wrapperCtrl.setLoadSpinner(scope);
      }
    };
  }).directive('djangoCradminModelChoiceFieldIframe', function() {
    return {
      require: '^djangoCradminModelChoiceFieldIframeWrapper',
      restrict: 'A',
      scope: {},
      controller: function($scope) {
        $scope.afterFieldValueChange = function() {};
        $scope.beforeShowingIframe = function(iframeSrc) {
          var currentSrc;
          currentSrc = $scope.element.attr('src');
          if ((currentSrc == null) || currentSrc === '' || currentSrc !== iframeSrc) {
            $scope.loadedSrc = currentSrc;
            $scope.wrapperCtrl.onIframeLoadBegin();
            $scope.resetIframeSize();
            return $scope.element.attr('src', iframeSrc);
          }
        };
        $scope.setIframeSize = function() {
          var iframeBodyHeight, iframeDocument, iframeWindow;
          iframeWindow = $scope.element.contents();
          iframeDocument = iframeWindow[0];
          if (iframeDocument != null) {
            iframeBodyHeight = iframeDocument.body.offsetHeight;
            return $scope.element.height(iframeBodyHeight + 60);
          }
        };
        return $scope.resetIframeSize = function() {
          return $scope.element.height('40px');
        };
      },
      link: function(scope, element, attrs, wrapperCtrl) {
        scope.element = element;
        scope.wrapperCtrl = wrapperCtrl;
        wrapperCtrl.setIframe(scope);
        scope.element.on('load', function() {
          wrapperCtrl.onIframeLoaded();
          return scope.setIframeSize();
        });
      }
    };
  }).directive('djangoCradminModelChoiceFieldWrapper', [
    'djangoCradminModelChoiceFieldCoordinator', function(djangoCradminModelChoiceFieldCoordinator) {
      return {
        restrict: 'A',
        scope: {
          iframeSrc: '@djangoCradminModelChoiceFieldWrapper'
        },
        controller: function($scope) {
          this.setField = function(fieldScope) {
            return $scope.fieldScope = fieldScope;
          };
          this.setPreviewElement = function(previewElementScope) {
            return $scope.previewElementScope = previewElementScope;
          };
          this.onChangeValueBegin = function() {
            return djangoCradminModelChoiceFieldCoordinator.onChangeValueBegin($scope);
          };
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldInput', [
    'djangoCradminModelChoiceFieldCoordinator', function(djangoCradminModelChoiceFieldCoordinator) {
      return {
        require: '^^djangoCradminModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.setValue = function(value) {
            return $scope.inputElement.val(value);
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.inputElement = element;
          scope.fieldid = attrs['id'];
          wrapperCtrl.setField(scope);
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldPreview', [
    'djangoCradminModelChoiceFieldCoordinator', function(djangoCradminModelChoiceFieldCoordinator) {
      return {
        require: '^^djangoCradminModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.setPreviewHtml = function(previewHtml) {
            return $scope.previewElement.html(previewHtml);
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.previewElement = element;
          wrapperCtrl.setPreviewElement(scope);
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldChangebeginButton', [
    'djangoCradminModelChoiceFieldCoordinator', function(djangoCradminModelChoiceFieldCoordinator) {
      return {
        require: '^^djangoCradminModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        link: function(scope, element, attrs, wrapperCtrl) {
          element.on('click', function(e) {
            e.preventDefault();
            return wrapperCtrl.onChangeValueBegin();
          });
        }
      };
    }
  ]);

}).call(this);
