/**
 * @license AngularJS v1.3.17
 * (c) 2010-2014 Google, Inc. http://angularjs.org
 * License: MIT
 */
(function(window, angular, undefined) {

'use strict';

/**
 * @ngdoc object
 * @name angular.mock
 * @description
 *
 * Namespace from 'angular-mocks.js' which contains testing related code.
 */
angular.mock = {};

/**
 * ! This is a private undocumented service !
 *
 * @name $browser
 *
 * @description
 * This service is a mock implementation of {@link ng.$browser}. It provides fake
 * implementation for commonly used browser apis that are hard to test, e.g. setTimeout, xhr,
 * cookies, etc...
 *
 * The api of this service is the same as that of the real {@link ng.$browser $browser}, except
 * that there are several helper methods available which can be used in tests.
 */
angular.mock.$BrowserProvider = function() {
  this.$get = function() {
    return new angular.mock.$Browser();
  };
};

angular.mock.$Browser = function() {
  var self = this;

  this.isMock = true;
  self.$$url = "http://server/";
  self.$$lastUrl = self.$$url; // used by url polling fn
  self.pollFns = [];

  // TODO(vojta): remove this temporary api
  self.$$completeOutstandingRequest = angular.noop;
  self.$$incOutstandingRequestCount = angular.noop;


  // register url polling fn

  self.onUrlChange = function(listener) {
    self.pollFns.push(
      function() {
        if (self.$$lastUrl !== self.$$url || self.$$state !== self.$$lastState) {
          self.$$lastUrl = self.$$url;
          self.$$lastState = self.$$state;
          listener(self.$$url, self.$$state);
        }
      }
    );

    return listener;
  };

  self.$$checkUrlChange = angular.noop;

  self.cookieHash = {};
  self.lastCookieHash = {};
  self.deferredFns = [];
  self.deferredNextId = 0;

  self.defer = function(fn, delay) {
    delay = delay || 0;
    self.deferredFns.push({time:(self.defer.now + delay), fn:fn, id: self.deferredNextId});
    self.deferredFns.sort(function(a, b) { return a.time - b.time;});
    return self.deferredNextId++;
  };


  /**
   * @name $browser#defer.now
   *
   * @description
   * Current milliseconds mock time.
   */
  self.defer.now = 0;


  self.defer.cancel = function(deferId) {
    var fnIndex;

    angular.forEach(self.deferredFns, function(fn, index) {
      if (fn.id === deferId) fnIndex = index;
    });

    if (fnIndex !== undefined) {
      self.deferredFns.splice(fnIndex, 1);
      return true;
    }

    return false;
  };


  /**
   * @name $browser#defer.flush
   *
   * @description
   * Flushes all pending requests and executes the defer callbacks.
   *
   * @param {number=} number of milliseconds to flush. See {@link #defer.now}
   */
  self.defer.flush = function(delay) {
    if (angular.isDefined(delay)) {
      self.defer.now += delay;
    } else {
      if (self.deferredFns.length) {
        self.defer.now = self.deferredFns[self.deferredFns.length - 1].time;
      } else {
        throw new Error('No deferred tasks to be flushed');
      }
    }

    while (self.deferredFns.length && self.deferredFns[0].time <= self.defer.now) {
      self.deferredFns.shift().fn();
    }
  };

  self.$$baseHref = '/';
  self.baseHref = function() {
    return this.$$baseHref;
  };
};
angular.mock.$Browser.prototype = {

/**
  * @name $browser#poll
  *
  * @description
  * run all fns in pollFns
  */
  poll: function poll() {
    angular.forEach(this.pollFns, function(pollFn) {
      pollFn();
    });
  },

  addPollFn: function(pollFn) {
    this.pollFns.push(pollFn);
    return pollFn;
  },

  url: function(url, replace, state) {
    if (angular.isUndefined(state)) {
      state = null;
    }
    if (url) {
      this.$$url = url;
      // Native pushState serializes & copies the object; simulate it.
      this.$$state = angular.copy(state);
      return this;
    }

    return this.$$url;
  },

  state: function() {
    return this.$$state;
  },

  cookies:  function(name, value) {
    if (name) {
      if (angular.isUndefined(value)) {
        delete this.cookieHash[name];
      } else {
        if (angular.isString(value) &&       //strings only
            value.length <= 4096) {          //strict cookie storage limits
          this.cookieHash[name] = value;
        }
      }
    } else {
      if (!angular.equals(this.cookieHash, this.lastCookieHash)) {
        this.lastCookieHash = angular.copy(this.cookieHash);
        this.cookieHash = angular.copy(this.cookieHash);
      }
      return this.cookieHash;
    }
  },

  notifyWhenNoOutstandingRequests: function(fn) {
    fn();
  }
};


/**
 * @ngdoc provider
 * @name $exceptionHandlerProvider
 *
 * @description
 * Configures the mock implementation of {@link ng.$exceptionHandler} to rethrow or to log errors
 * passed to the `$exceptionHandler`.
 */

/**
 * @ngdoc service
 * @name $exceptionHandler
 *
 * @description
 * Mock implementation of {@link ng.$exceptionHandler} that rethrows or logs errors passed
 * to it. See {@link ngMock.$exceptionHandlerProvider $exceptionHandlerProvider} for configuration
 * information.
 *
 *
 * ```js
 *   describe('$exceptionHandlerProvider', function() {
 *
 *     it('should capture log messages and exceptions', function() {
 *
 *       module(function($exceptionHandlerProvider) {
 *         $exceptionHandlerProvider.mode('log');
 *       });
 *
 *       inject(function($log, $exceptionHandler, $timeout) {
 *         $timeout(function() { $log.log(1); });
 *         $timeout(function() { $log.log(2); throw 'banana peel'; });
 *         $timeout(function() { $log.log(3); });
 *         expect($exceptionHandler.errors).toEqual([]);
 *         expect($log.assertEmpty());
 *         $timeout.flush();
 *         expect($exceptionHandler.errors).toEqual(['banana peel']);
 *         expect($log.log.logs).toEqual([[1], [2], [3]]);
 *       });
 *     });
 *   });
 * ```
 */

angular.mock.$ExceptionHandlerProvider = function() {
  var handler;

  /**
   * @ngdoc method
   * @name $exceptionHandlerProvider#mode
   *
   * @description
   * Sets the logging mode.
   *
   * @param {string} mode Mode of operation, defaults to `rethrow`.
   *
   *   - `log`: Sometimes it is desirable to test that an error is thrown, for this case the `log`
   *            mode stores an array of errors in `$exceptionHandler.errors`, to allow later
   *            assertion of them. See {@link ngMock.$log#assertEmpty assertEmpty()} and
   *            {@link ngMock.$log#reset reset()}
   *   - `rethrow`: If any errors are passed to the handler in tests, it typically means that there
   *                is a bug in the application or test, so this mock will make these tests fail.
   *                For any implementations that expect exceptions to be thrown, the `rethrow` mode
   *                will also maintain a log of thrown errors.
   */
  this.mode = function(mode) {

    switch (mode) {
      case 'log':
      case 'rethrow':
        var errors = [];
        handler = function(e) {
          if (arguments.length == 1) {
            errors.push(e);
          } else {
            errors.push([].slice.call(arguments, 0));
          }
          if (mode === "rethrow") {
            throw e;
          }
        };
        handler.errors = errors;
        break;
      default:
        throw new Error("Unknown mode '" + mode + "', only 'log'/'rethrow' modes are allowed!");
    }
  };

  this.$get = function() {
    return handler;
  };

  this.mode('rethrow');
};


/**
 * @ngdoc service
 * @name $log
 *
 * @description
 * Mock implementation of {@link ng.$log} that gathers all logged messages in arrays
 * (one array per logging level). These arrays are exposed as `logs` property of each of the
 * level-specific log function, e.g. for level `error` the array is exposed as `$log.error.logs`.
 *
 */
angular.mock.$LogProvider = function() {
  var debug = true;

  function concat(array1, array2, index) {
    return array1.concat(Array.prototype.slice.call(array2, index));
  }

  this.debugEnabled = function(flag) {
    if (angular.isDefined(flag)) {
      debug = flag;
      return this;
    } else {
      return debug;
    }
  };

  this.$get = function() {
    var $log = {
      log: function() { $log.log.logs.push(concat([], arguments, 0)); },
      warn: function() { $log.warn.logs.push(concat([], arguments, 0)); },
      info: function() { $log.info.logs.push(concat([], arguments, 0)); },
      error: function() { $log.error.logs.push(concat([], arguments, 0)); },
      debug: function() {
        if (debug) {
          $log.debug.logs.push(concat([], arguments, 0));
        }
      }
    };

    /**
     * @ngdoc method
     * @name $log#reset
     *
     * @description
     * Reset all of the logging arrays to empty.
     */
    $log.reset = function() {
      /**
       * @ngdoc property
       * @name $log#log.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#log `log()`}.
       *
       * @example
       * ```js
       * $log.log('Some Log');
       * var first = $log.log.logs.unshift();
       * ```
       */
      $log.log.logs = [];
      /**
       * @ngdoc property
       * @name $log#info.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#info `info()`}.
       *
       * @example
       * ```js
       * $log.info('Some Info');
       * var first = $log.info.logs.unshift();
       * ```
       */
      $log.info.logs = [];
      /**
       * @ngdoc property
       * @name $log#warn.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#warn `warn()`}.
       *
       * @example
       * ```js
       * $log.warn('Some Warning');
       * var first = $log.warn.logs.unshift();
       * ```
       */
      $log.warn.logs = [];
      /**
       * @ngdoc property
       * @name $log#error.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#error `error()`}.
       *
       * @example
       * ```js
       * $log.error('Some Error');
       * var first = $log.error.logs.unshift();
       * ```
       */
      $log.error.logs = [];
        /**
       * @ngdoc property
       * @name $log#debug.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#debug `debug()`}.
       *
       * @example
       * ```js
       * $log.debug('Some Error');
       * var first = $log.debug.logs.unshift();
       * ```
       */
      $log.debug.logs = [];
    };

    /**
     * @ngdoc method
     * @name $log#assertEmpty
     *
     * @description
     * Assert that all of the logging methods have no logged messages. If any messages are present,
     * an exception is thrown.
     */
    $log.assertEmpty = function() {
      var errors = [];
      angular.forEach(['error', 'warn', 'info', 'log', 'debug'], function(logLevel) {
        angular.forEach($log[logLevel].logs, function(log) {
          angular.forEach(log, function(logItem) {
            errors.push('MOCK $log (' + logLevel + '): ' + String(logItem) + '\n' +
                        (logItem.stack || ''));
          });
        });
      });
      if (errors.length) {
        errors.unshift("Expected $log to be empty! Either a message was logged unexpectedly, or " +
          "an expected log message was not checked and removed:");
        errors.push('');
        throw new Error(errors.join('\n---------\n'));
      }
    };

    $log.reset();
    return $log;
  };
};


/**
 * @ngdoc service
 * @name $interval
 *
 * @description
 * Mock implementation of the $interval service.
 *
 * Use {@link ngMock.$interval#flush `$interval.flush(millis)`} to
 * move forward by `millis` milliseconds and trigger any functions scheduled to run in that
 * time.
 *
 * @param {function()} fn A function that should be called repeatedly.
 * @param {number} delay Number of milliseconds between each function call.
 * @param {number=} [count=0] Number of times to repeat. If not set, or 0, will repeat
 *   indefinitely.
 * @param {boolean=} [invokeApply=true] If set to `false` skips model dirty checking, otherwise
 *   will invoke `fn` within the {@link ng.$rootScope.Scope#$apply $apply} block.
 * @returns {promise} A promise which will be notified on each iteration.
 */
angular.mock.$IntervalProvider = function() {
  this.$get = ['$browser', '$rootScope', '$q', '$$q',
       function($browser,   $rootScope,   $q,   $$q) {
    var repeatFns = [],
        nextRepeatId = 0,
        now = 0;

    var $interval = function(fn, delay, count, invokeApply) {
      var iteration = 0,
          skipApply = (angular.isDefined(invokeApply) && !invokeApply),
          deferred = (skipApply ? $$q : $q).defer(),
          promise = deferred.promise;

      count = (angular.isDefined(count)) ? count : 0;
      promise.then(null, null, fn);

      promise.$$intervalId = nextRepeatId;

      function tick() {
        deferred.notify(iteration++);

        if (count > 0 && iteration >= count) {
          var fnIndex;
          deferred.resolve(iteration);

          angular.forEach(repeatFns, function(fn, index) {
            if (fn.id === promise.$$intervalId) fnIndex = index;
          });

          if (fnIndex !== undefined) {
            repeatFns.splice(fnIndex, 1);
          }
        }

        if (skipApply) {
          $browser.defer.flush();
        } else {
          $rootScope.$apply();
        }
      }

      repeatFns.push({
        nextTime:(now + delay),
        delay: delay,
        fn: tick,
        id: nextRepeatId,
        deferred: deferred
      });
      repeatFns.sort(function(a, b) { return a.nextTime - b.nextTime;});

      nextRepeatId++;
      return promise;
    };
    /**
     * @ngdoc method
     * @name $interval#cancel
     *
     * @description
     * Cancels a task associated with the `promise`.
     *
     * @param {promise} promise A promise from calling the `$interval` function.
     * @returns {boolean} Returns `true` if the task was successfully cancelled.
     */
    $interval.cancel = function(promise) {
      if (!promise) return false;
      var fnIndex;

      angular.forEach(repeatFns, function(fn, index) {
        if (fn.id === promise.$$intervalId) fnIndex = index;
      });

      if (fnIndex !== undefined) {
        repeatFns[fnIndex].deferred.reject('canceled');
        repeatFns.splice(fnIndex, 1);
        return true;
      }

      return false;
    };

    /**
     * @ngdoc method
     * @name $interval#flush
     * @description
     *
     * Runs interval tasks scheduled to be run in the next `millis` milliseconds.
     *
     * @param {number=} millis maximum timeout amount to flush up until.
     *
     * @return {number} The amount of time moved forward.
     */
    $interval.flush = function(millis) {
      now += millis;
      while (repeatFns.length && repeatFns[0].nextTime <= now) {
        var task = repeatFns[0];
        task.fn();
        task.nextTime += task.delay;
        repeatFns.sort(function(a, b) { return a.nextTime - b.nextTime;});
      }
      return millis;
    };

    return $interval;
  }];
};


/* jshint -W101 */
/* The R_ISO8061_STR regex is never going to fit into the 100 char limit!
 * This directive should go inside the anonymous function but a bug in JSHint means that it would
 * not be enacted early enough to prevent the warning.
 */
var R_ISO8061_STR = /^(\d{4})-?(\d\d)-?(\d\d)(?:T(\d\d)(?:\:?(\d\d)(?:\:?(\d\d)(?:\.(\d{3}))?)?)?(Z|([+-])(\d\d):?(\d\d)))?$/;

function jsonStringToDate(string) {
  var match;
  if (match = string.match(R_ISO8061_STR)) {
    var date = new Date(0),
        tzHour = 0,
        tzMin  = 0;
    if (match[9]) {
      tzHour = int(match[9] + match[10]);
      tzMin = int(match[9] + match[11]);
    }
    date.setUTCFullYear(int(match[1]), int(match[2]) - 1, int(match[3]));
    date.setUTCHours(int(match[4] || 0) - tzHour,
                     int(match[5] || 0) - tzMin,
                     int(match[6] || 0),
                     int(match[7] || 0));
    return date;
  }
  return string;
}

function int(str) {
  return parseInt(str, 10);
}

function padNumber(num, digits, trim) {
  var neg = '';
  if (num < 0) {
    neg =  '-';
    num = -num;
  }
  num = '' + num;
  while (num.length < digits) num = '0' + num;
  if (trim)
    num = num.substr(num.length - digits);
  return neg + num;
}


/**
 * @ngdoc type
 * @name angular.mock.TzDate
 * @description
 *
 * *NOTE*: this is not an injectable instance, just a globally available mock class of `Date`.
 *
 * Mock of the Date type which has its timezone specified via constructor arg.
 *
 * The main purpose is to create Date-like instances with timezone fixed to the specified timezone
 * offset, so that we can test code that depends on local timezone settings without dependency on
 * the time zone settings of the machine where the code is running.
 *
 * @param {number} offset Offset of the *desired* timezone in hours (fractions will be honored)
 * @param {(number|string)} timestamp Timestamp representing the desired time in *UTC*
 *
 * @example
 * !!!! WARNING !!!!!
 * This is not a complete Date object so only methods that were implemented can be called safely.
 * To make matters worse, TzDate instances inherit stuff from Date via a prototype.
 *
 * We do our best to intercept calls to "unimplemented" methods, but since the list of methods is
 * incomplete we might be missing some non-standard methods. This can result in errors like:
 * "Date.prototype.foo called on incompatible Object".
 *
 * ```js
 * var newYearInBratislava = new TzDate(-1, '2009-12-31T23:00:00Z');
 * newYearInBratislava.getTimezoneOffset() => -60;
 * newYearInBratislava.getFullYear() => 2010;
 * newYearInBratislava.getMonth() => 0;
 * newYearInBratislava.getDate() => 1;
 * newYearInBratislava.getHours() => 0;
 * newYearInBratislava.getMinutes() => 0;
 * newYearInBratislava.getSeconds() => 0;
 * ```
 *
 */
angular.mock.TzDate = function(offset, timestamp) {
  var self = new Date(0);
  if (angular.isString(timestamp)) {
    var tsStr = timestamp;

    self.origDate = jsonStringToDate(timestamp);

    timestamp = self.origDate.getTime();
    if (isNaN(timestamp))
      throw {
        name: "Illegal Argument",
        message: "Arg '" + tsStr + "' passed into TzDate constructor is not a valid date string"
      };
  } else {
    self.origDate = new Date(timestamp);
  }

  var localOffset = new Date(timestamp).getTimezoneOffset();
  self.offsetDiff = localOffset * 60 * 1000 - offset * 1000 * 60 * 60;
  self.date = new Date(timestamp + self.offsetDiff);

  self.getTime = function() {
    return self.date.getTime() - self.offsetDiff;
  };

  self.toLocaleDateString = function() {
    return self.date.toLocaleDateString();
  };

  self.getFullYear = function() {
    return self.date.getFullYear();
  };

  self.getMonth = function() {
    return self.date.getMonth();
  };

  self.getDate = function() {
    return self.date.getDate();
  };

  self.getHours = function() {
    return self.date.getHours();
  };

  self.getMinutes = function() {
    return self.date.getMinutes();
  };

  self.getSeconds = function() {
    return self.date.getSeconds();
  };

  self.getMilliseconds = function() {
    return self.date.getMilliseconds();
  };

  self.getTimezoneOffset = function() {
    return offset * 60;
  };

  self.getUTCFullYear = function() {
    return self.origDate.getUTCFullYear();
  };

  self.getUTCMonth = function() {
    return self.origDate.getUTCMonth();
  };

  self.getUTCDate = function() {
    return self.origDate.getUTCDate();
  };

  self.getUTCHours = function() {
    return self.origDate.getUTCHours();
  };

  self.getUTCMinutes = function() {
    return self.origDate.getUTCMinutes();
  };

  self.getUTCSeconds = function() {
    return self.origDate.getUTCSeconds();
  };

  self.getUTCMilliseconds = function() {
    return self.origDate.getUTCMilliseconds();
  };

  self.getDay = function() {
    return self.date.getDay();
  };

  // provide this method only on browsers that already have it
  if (self.toISOString) {
    self.toISOString = function() {
      return padNumber(self.origDate.getUTCFullYear(), 4) + '-' +
            padNumber(self.origDate.getUTCMonth() + 1, 2) + '-' +
            padNumber(self.origDate.getUTCDate(), 2) + 'T' +
            padNumber(self.origDate.getUTCHours(), 2) + ':' +
            padNumber(self.origDate.getUTCMinutes(), 2) + ':' +
            padNumber(self.origDate.getUTCSeconds(), 2) + '.' +
            padNumber(self.origDate.getUTCMilliseconds(), 3) + 'Z';
    };
  }

  //hide all methods not implemented in this mock that the Date prototype exposes
  var unimplementedMethods = ['getUTCDay',
      'getYear', 'setDate', 'setFullYear', 'setHours', 'setMilliseconds',
      'setMinutes', 'setMonth', 'setSeconds', 'setTime', 'setUTCDate', 'setUTCFullYear',
      'setUTCHours', 'setUTCMilliseconds', 'setUTCMinutes', 'setUTCMonth', 'setUTCSeconds',
      'setYear', 'toDateString', 'toGMTString', 'toJSON', 'toLocaleFormat', 'toLocaleString',
      'toLocaleTimeString', 'toSource', 'toString', 'toTimeString', 'toUTCString', 'valueOf'];

  angular.forEach(unimplementedMethods, function(methodName) {
    self[methodName] = function() {
      throw new Error("Method '" + methodName + "' is not implemented in the TzDate mock");
    };
  });

  return self;
};

//make "tzDateInstance instanceof Date" return true
angular.mock.TzDate.prototype = Date.prototype;
/* jshint +W101 */

angular.mock.animate = angular.module('ngAnimateMock', ['ng'])

  .config(['$provide', function($provide) {

    var reflowQueue = [];
    $provide.value('$$animateReflow', function(fn) {
      var index = reflowQueue.length;
      reflowQueue.push(fn);
      return function cancel() {
        reflowQueue.splice(index, 1);
      };
    });

    $provide.decorator('$animate', ['$delegate', '$$asyncCallback', '$timeout', '$browser',
                            function($delegate,   $$asyncCallback,   $timeout,   $browser) {
      var animate = {
        queue: [],
        cancel: $delegate.cancel,
        enabled: $delegate.enabled,
        triggerCallbackEvents: function() {
          $$asyncCallback.flush();
        },
        triggerCallbackPromise: function() {
          $timeout.flush(0);
        },
        triggerCallbacks: function() {
          this.triggerCallbackEvents();
          this.triggerCallbackPromise();
        },
        triggerReflow: function() {
          angular.forEach(reflowQueue, function(fn) {
            fn();
          });
          reflowQueue = [];
        }
      };

      angular.forEach(
        ['animate','enter','leave','move','addClass','removeClass','setClass'], function(method) {
        animate[method] = function() {
          animate.queue.push({
            event: method,
            element: arguments[0],
            options: arguments[arguments.length - 1],
            args: arguments
          });
          return $delegate[method].apply($delegate, arguments);
        };
      });

      return animate;
    }]);

  }]);


/**
 * @ngdoc function
 * @name angular.mock.dump
 * @description
 *
 * *NOTE*: this is not an injectable instance, just a globally available function.
 *
 * Method for serializing common angular objects (scope, elements, etc..) into strings, useful for
 * debugging.
 *
 * This method is also available on window, where it can be used to display objects on debug
 * console.
 *
 * @param {*} object - any object to turn into string.
 * @return {string} a serialized string of the argument
 */
angular.mock.dump = function(object) {
  return serialize(object);

  function serialize(object) {
    var out;

    if (angular.isElement(object)) {
      object = angular.element(object);
      out = angular.element('<div></div>');
      angular.forEach(object, function(element) {
        out.append(angular.element(element).clone());
      });
      out = out.html();
    } else if (angular.isArray(object)) {
      out = [];
      angular.forEach(object, function(o) {
        out.push(serialize(o));
      });
      out = '[ ' + out.join(', ') + ' ]';
    } else if (angular.isObject(object)) {
      if (angular.isFunction(object.$eval) && angular.isFunction(object.$apply)) {
        out = serializeScope(object);
      } else if (object instanceof Error) {
        out = object.stack || ('' + object.name + ': ' + object.message);
      } else {
        // TODO(i): this prevents methods being logged,
        // we should have a better way to serialize objects
        out = angular.toJson(object, true);
      }
    } else {
      out = String(object);
    }

    return out;
  }

  function serializeScope(scope, offset) {
    offset = offset ||  '  ';
    var log = [offset + 'Scope(' + scope.$id + '): {'];
    for (var key in scope) {
      if (Object.prototype.hasOwnProperty.call(scope, key) && !key.match(/^(\$|this)/)) {
        log.push('  ' + key + ': ' + angular.toJson(scope[key]));
      }
    }
    var child = scope.$$childHead;
    while (child) {
      log.push(serializeScope(child, offset + '  '));
      child = child.$$nextSibling;
    }
    log.push('}');
    return log.join('\n' + offset);
  }
};

/**
 * @ngdoc service
 * @name $httpBackend
 * @description
 * Fake HTTP backend implementation suitable for unit testing applications that use the
 * {@link ng.$http $http service}.
 *
 * *Note*: For fake HTTP backend implementation suitable for end-to-end testing or backend-less
 * development please see {@link ngMockE2E.$httpBackend e2e $httpBackend mock}.
 *
 * During unit testing, we want our unit tests to run quickly and have no external dependencies so
 * we don’t want to send [XHR](https://developer.mozilla.org/en/xmlhttprequest) or
 * [JSONP](http://en.wikipedia.org/wiki/JSONP) requests to a real server. All we really need is
 * to verify whether a certain request has been sent or not, or alternatively just let the
 * application make requests, respond with pre-trained responses and assert that the end result is
 * what we expect it to be.
 *
 * This mock implementation can be used to respond with static or dynamic responses via the
 * `expect` and `when` apis and their shortcuts (`expectGET`, `whenPOST`, etc).
 *
 * When an Angular application needs some data from a server, it calls the $http service, which
 * sends the request to a real server using $httpBackend service. With dependency injection, it is
 * easy to inject $httpBackend mock (which has the same API as $httpBackend) and use it to verify
 * the requests and respond with some testing data without sending a request to a real server.
 *
 * There are two ways to specify what test data should be returned as http responses by the mock
 * backend when the code under test makes http requests:
 *
 * - `$httpBackend.expect` - specifies a request expectation
 * - `$httpBackend.when` - specifies a backend definition
 *
 *
 * # Request Expectations vs Backend Definitions
 *
 * Request expectations provide a way to make assertions about requests made by the application and
 * to define responses for those requests. The test will fail if the expected requests are not made
 * or they are made in the wrong order.
 *
 * Backend definitions allow you to define a fake backend for your application which doesn't assert
 * if a particular request was made or not, it just returns a trained response if a request is made.
 * The test will pass whether or not the request gets made during testing.
 *
 *
 * <table class="table">
 *   <tr><th width="220px"></th><th>Request expectations</th><th>Backend definitions</th></tr>
 *   <tr>
 *     <th>Syntax</th>
 *     <td>.expect(...).respond(...)</td>
 *     <td>.when(...).respond(...)</td>
 *   </tr>
 *   <tr>
 *     <th>Typical usage</th>
 *     <td>strict unit tests</td>
 *     <td>loose (black-box) unit testing</td>
 *   </tr>
 *   <tr>
 *     <th>Fulfills multiple requests</th>
 *     <td>NO</td>
 *     <td>YES</td>
 *   </tr>
 *   <tr>
 *     <th>Order of requests matters</th>
 *     <td>YES</td>
 *     <td>NO</td>
 *   </tr>
 *   <tr>
 *     <th>Request required</th>
 *     <td>YES</td>
 *     <td>NO</td>
 *   </tr>
 *   <tr>
 *     <th>Response required</th>
 *     <td>optional (see below)</td>
 *     <td>YES</td>
 *   </tr>
 * </table>
 *
 * In cases where both backend definitions and request expectations are specified during unit
 * testing, the request expectations are evaluated first.
 *
 * If a request expectation has no response specified, the algorithm will search your backend
 * definitions for an appropriate response.
 *
 * If a request didn't match any expectation or if the expectation doesn't have the response
 * defined, the backend definitions are evaluated in sequential order to see if any of them match
 * the request. The response from the first matched definition is returned.
 *
 *
 * # Flushing HTTP requests
 *
 * The $httpBackend used in production always responds to requests asynchronously. If we preserved
 * this behavior in unit testing, we'd have to create async unit tests, which are hard to write,
 * to follow and to maintain. But neither can the testing mock respond synchronously; that would
 * change the execution of the code under test. For this reason, the mock $httpBackend has a
 * `flush()` method, which allows the test to explicitly flush pending requests. This preserves
 * the async api of the backend, while allowing the test to execute synchronously.
 *
 *
 * # Unit testing with mock $httpBackend
 * The following code shows how to setup and use the mock backend when unit testing a controller.
 * First we create the controller under test:
 *
  ```js
  // The module code
  angular
    .module('MyApp', [])
    .controller('MyController', MyController);

  // The controller code
  function MyController($scope, $http) {
    var authToken;

    $http.get('/auth.py').success(function(data, status, headers) {
      authToken = headers('A-Token');
      $scope.user = data;
    });

    $scope.saveMessage = function(message) {
      var headers = { 'Authorization': authToken };
      $scope.status = 'Saving...';

      $http.post('/add-msg.py', message, { headers: headers } ).success(function(response) {
        $scope.status = '';
      }).error(function() {
        $scope.status = 'ERROR!';
      });
    };
  }
  ```
 *
 * Now we setup the mock backend and create the test specs:
 *
  ```js
    // testing controller
    describe('MyController', function() {
       var $httpBackend, $rootScope, createController, authRequestHandler;

       // Set up the module
       beforeEach(module('MyApp'));

       beforeEach(inject(function($injector) {
         // Set up the mock http service responses
         $httpBackend = $injector.get('$httpBackend');
         // backend definition common for all tests
         authRequestHandler = $httpBackend.when('GET', '/auth.py')
                                .respond({userId: 'userX'}, {'A-Token': 'xxx'});

         // Get hold of a scope (i.e. the root scope)
         $rootScope = $injector.get('$rootScope');
         // The $controller service is used to create instances of controllers
         var $controller = $injector.get('$controller');

         createController = function() {
           return $controller('MyController', {'$scope' : $rootScope });
         };
       }));


       afterEach(function() {
         $httpBackend.verifyNoOutstandingExpectation();
         $httpBackend.verifyNoOutstandingRequest();
       });


       it('should fetch authentication token', function() {
         $httpBackend.expectGET('/auth.py');
         var controller = createController();
         $httpBackend.flush();
       });


       it('should fail authentication', function() {

         // Notice how you can change the response even after it was set
         authRequestHandler.respond(401, '');

         $httpBackend.expectGET('/auth.py');
         var controller = createController();
         $httpBackend.flush();
         expect($rootScope.status).toBe('Failed...');
       });


       it('should send msg to server', function() {
         var controller = createController();
         $httpBackend.flush();

         // now you don’t care about the authentication, but
         // the controller will still send the request and
         // $httpBackend will respond without you having to
         // specify the expectation and response for this request

         $httpBackend.expectPOST('/add-msg.py', 'message content').respond(201, '');
         $rootScope.saveMessage('message content');
         expect($rootScope.status).toBe('Saving...');
         $httpBackend.flush();
         expect($rootScope.status).toBe('');
       });


       it('should send auth header', function() {
         var controller = createController();
         $httpBackend.flush();

         $httpBackend.expectPOST('/add-msg.py', undefined, function(headers) {
           // check if the header was send, if it wasn't the expectation won't
           // match the request and the test will fail
           return headers['Authorization'] == 'xxx';
         }).respond(201, '');

         $rootScope.saveMessage('whatever');
         $httpBackend.flush();
       });
    });
   ```
 */
angular.mock.$HttpBackendProvider = function() {
  this.$get = ['$rootScope', '$timeout', createHttpBackendMock];
};

/**
 * General factory function for $httpBackend mock.
 * Returns instance for unit testing (when no arguments specified):
 *   - passing through is disabled
 *   - auto flushing is disabled
 *
 * Returns instance for e2e testing (when `$delegate` and `$browser` specified):
 *   - passing through (delegating request to real backend) is enabled
 *   - auto flushing is enabled
 *
 * @param {Object=} $delegate Real $httpBackend instance (allow passing through if specified)
 * @param {Object=} $browser Auto-flushing enabled if specified
 * @return {Object} Instance of $httpBackend mock
 */
function createHttpBackendMock($rootScope, $timeout, $delegate, $browser) {
  var definitions = [],
      expectations = [],
      responses = [],
      responsesPush = angular.bind(responses, responses.push),
      copy = angular.copy;

  function createResponse(status, data, headers, statusText) {
    if (angular.isFunction(status)) return status;

    return function() {
      return angular.isNumber(status)
          ? [status, data, headers, statusText]
          : [200, status, data, headers];
    };
  }

  // TODO(vojta): change params to: method, url, data, headers, callback
  function $httpBackend(method, url, data, callback, headers, timeout, withCredentials) {
    var xhr = new MockXhr(),
        expectation = expectations[0],
        wasExpected = false;

    function prettyPrint(data) {
      return (angular.isString(data) || angular.isFunction(data) || data instanceof RegExp)
          ? data
          : angular.toJson(data);
    }

    function wrapResponse(wrapped) {
      if (!$browser && timeout) {
        timeout.then ? timeout.then(handleTimeout) : $timeout(handleTimeout, timeout);
      }

      return handleResponse;

      function handleResponse() {
        var response = wrapped.response(method, url, data, headers);
        xhr.$$respHeaders = response[2];
        callback(copy(response[0]), copy(response[1]), xhr.getAllResponseHeaders(),
                 copy(response[3] || ''));
      }

      function handleTimeout() {
        for (var i = 0, ii = responses.length; i < ii; i++) {
          if (responses[i] === handleResponse) {
            responses.splice(i, 1);
            callback(-1, undefined, '');
            break;
          }
        }
      }
    }

    if (expectation && expectation.match(method, url)) {
      if (!expectation.matchData(data))
        throw new Error('Expected ' + expectation + ' with different data\n' +
            'EXPECTED: ' + prettyPrint(expectation.data) + '\nGOT:      ' + data);

      if (!expectation.matchHeaders(headers))
        throw new Error('Expected ' + expectation + ' with different headers\n' +
                        'EXPECTED: ' + prettyPrint(expectation.headers) + '\nGOT:      ' +
                        prettyPrint(headers));

      expectations.shift();

      if (expectation.response) {
        responses.push(wrapResponse(expectation));
        return;
      }
      wasExpected = true;
    }

    var i = -1, definition;
    while ((definition = definitions[++i])) {
      if (definition.match(method, url, data, headers || {})) {
        if (definition.response) {
          // if $browser specified, we do auto flush all requests
          ($browser ? $browser.defer : responsesPush)(wrapResponse(definition));
        } else if (definition.passThrough) {
          $delegate(method, url, data, callback, headers, timeout, withCredentials);
        } else throw new Error('No response defined !');
        return;
      }
    }
    throw wasExpected ?
        new Error('No response defined !') :
        new Error('Unexpected request: ' + method + ' ' + url + '\n' +
                  (expectation ? 'Expected ' + expectation : 'No more request expected'));
  }

  /**
   * @ngdoc method
   * @name $httpBackend#when
   * @description
   * Creates a new backend definition.
   *
   * @param {string} method HTTP method.
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
   *   object and returns true if the headers match the current definition.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   *
   *  - respond –
   *      `{function([status,] data[, headers, statusText])
   *      | function(function(method, url, data, headers)}`
   *    – The respond method takes a set of static data to be returned or a function that can
   *    return an array containing response status (number), response data (string), response
   *    headers (Object), and the text for the status (string). The respond method returns the
   *    `requestHandler` object for possible overrides.
   */
  $httpBackend.when = function(method, url, data, headers) {
    var definition = new MockHttpExpectation(method, url, data, headers),
        chain = {
          respond: function(status, data, headers, statusText) {
            definition.passThrough = undefined;
            definition.response = createResponse(status, data, headers, statusText);
            return chain;
          }
        };

    if ($browser) {
      chain.passThrough = function() {
        definition.response = undefined;
        definition.passThrough = true;
        return chain;
      };
    }

    definitions.push(definition);
    return chain;
  };

  /**
   * @ngdoc method
   * @name $httpBackend#whenGET
   * @description
   * Creates a new backend definition for GET requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenHEAD
   * @description
   * Creates a new backend definition for HEAD requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenDELETE
   * @description
   * Creates a new backend definition for DELETE requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenPOST
   * @description
   * Creates a new backend definition for POST requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenPUT
   * @description
   * Creates a new backend definition for PUT requests.  For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenJSONP
   * @description
   * Creates a new backend definition for JSONP requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */
  createShortMethods('when');


  /**
   * @ngdoc method
   * @name $httpBackend#expect
   * @description
   * Creates a new request expectation.
   *
   * @param {string} method HTTP method.
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
   *   object and returns true if the headers match the current expectation.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *  request is handled. You can save this object for later use and invoke `respond` again in
   *  order to change how a matched request is handled.
   *
   *  - respond –
   *    `{function([status,] data[, headers, statusText])
   *    | function(function(method, url, data, headers)}`
   *    – The respond method takes a set of static data to be returned or a function that can
   *    return an array containing response status (number), response data (string), response
   *    headers (Object), and the text for the status (string). The respond method returns the
   *    `requestHandler` object for possible overrides.
   */
  $httpBackend.expect = function(method, url, data, headers) {
    var expectation = new MockHttpExpectation(method, url, data, headers),
        chain = {
          respond: function(status, data, headers, statusText) {
            expectation.response = createResponse(status, data, headers, statusText);
            return chain;
          }
        };

    expectations.push(expectation);
    return chain;
  };


  /**
   * @ngdoc method
   * @name $httpBackend#expectGET
   * @description
   * Creates a new request expectation for GET requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled. See #expect for more info.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectHEAD
   * @description
   * Creates a new request expectation for HEAD requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectDELETE
   * @description
   * Creates a new request expectation for DELETE requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPOST
   * @description
   * Creates a new request expectation for POST requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPUT
   * @description
   * Creates a new request expectation for PUT requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPATCH
   * @description
   * Creates a new request expectation for PATCH requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectJSONP
   * @description
   * Creates a new request expectation for JSONP requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
   *   and returns true if the url match the current definition.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */
  createShortMethods('expect');


  /**
   * @ngdoc method
   * @name $httpBackend#flush
   * @description
   * Flushes all pending requests using the trained responses.
   *
   * @param {number=} count Number of responses to flush (in the order they arrived). If undefined,
   *   all pending requests will be flushed. If there are no pending requests when the flush method
   *   is called an exception is thrown (as this typically a sign of programming error).
   */
  $httpBackend.flush = function(count, digest) {
    if (digest !== false) $rootScope.$digest();
    if (!responses.length) throw new Error('No pending request to flush !');

    if (angular.isDefined(count) && count !== null) {
      while (count--) {
        if (!responses.length) throw new Error('No more pending request to flush !');
        responses.shift()();
      }
    } else {
      while (responses.length) {
        responses.shift()();
      }
    }
    $httpBackend.verifyNoOutstandingExpectation(digest);
  };


  /**
   * @ngdoc method
   * @name $httpBackend#verifyNoOutstandingExpectation
   * @description
   * Verifies that all of the requests defined via the `expect` api were made. If any of the
   * requests were not made, verifyNoOutstandingExpectation throws an exception.
   *
   * Typically, you would call this method following each test case that asserts requests using an
   * "afterEach" clause.
   *
   * ```js
   *   afterEach($httpBackend.verifyNoOutstandingExpectation);
   * ```
   */
  $httpBackend.verifyNoOutstandingExpectation = function(digest) {
    if (digest !== false) $rootScope.$digest();
    if (expectations.length) {
      throw new Error('Unsatisfied requests: ' + expectations.join(', '));
    }
  };


  /**
   * @ngdoc method
   * @name $httpBackend#verifyNoOutstandingRequest
   * @description
   * Verifies that there are no outstanding requests that need to be flushed.
   *
   * Typically, you would call this method following each test case that asserts requests using an
   * "afterEach" clause.
   *
   * ```js
   *   afterEach($httpBackend.verifyNoOutstandingRequest);
   * ```
   */
  $httpBackend.verifyNoOutstandingRequest = function() {
    if (responses.length) {
      throw new Error('Unflushed requests: ' + responses.length);
    }
  };


  /**
   * @ngdoc method
   * @name $httpBackend#resetExpectations
   * @description
   * Resets all request expectations, but preserves all backend definitions. Typically, you would
   * call resetExpectations during a multiple-phase test when you want to reuse the same instance of
   * $httpBackend mock.
   */
  $httpBackend.resetExpectations = function() {
    expectations.length = 0;
    responses.length = 0;
  };

  return $httpBackend;


  function createShortMethods(prefix) {
    angular.forEach(['GET', 'DELETE', 'JSONP', 'HEAD'], function(method) {
     $httpBackend[prefix + method] = function(url, headers) {
       return $httpBackend[prefix](method, url, undefined, headers);
     };
    });

    angular.forEach(['PUT', 'POST', 'PATCH'], function(method) {
      $httpBackend[prefix + method] = function(url, data, headers) {
        return $httpBackend[prefix](method, url, data, headers);
      };
    });
  }
}

function MockHttpExpectation(method, url, data, headers) {

  this.data = data;
  this.headers = headers;

  this.match = function(m, u, d, h) {
    if (method != m) return false;
    if (!this.matchUrl(u)) return false;
    if (angular.isDefined(d) && !this.matchData(d)) return false;
    if (angular.isDefined(h) && !this.matchHeaders(h)) return false;
    return true;
  };

  this.matchUrl = function(u) {
    if (!url) return true;
    if (angular.isFunction(url.test)) return url.test(u);
    if (angular.isFunction(url)) return url(u);
    return url == u;
  };

  this.matchHeaders = function(h) {
    if (angular.isUndefined(headers)) return true;
    if (angular.isFunction(headers)) return headers(h);
    return angular.equals(headers, h);
  };

  this.matchData = function(d) {
    if (angular.isUndefined(data)) return true;
    if (data && angular.isFunction(data.test)) return data.test(d);
    if (data && angular.isFunction(data)) return data(d);
    if (data && !angular.isString(data)) {
      return angular.equals(angular.fromJson(angular.toJson(data)), angular.fromJson(d));
    }
    return data == d;
  };

  this.toString = function() {
    return method + ' ' + url;
  };
}

function createMockXhr() {
  return new MockXhr();
}

function MockXhr() {

  // hack for testing $http, $httpBackend
  MockXhr.$$lastInstance = this;

  this.open = function(method, url, async) {
    this.$$method = method;
    this.$$url = url;
    this.$$async = async;
    this.$$reqHeaders = {};
    this.$$respHeaders = {};
  };

  this.send = function(data) {
    this.$$data = data;
  };

  this.setRequestHeader = function(key, value) {
    this.$$reqHeaders[key] = value;
  };

  this.getResponseHeader = function(name) {
    // the lookup must be case insensitive,
    // that's why we try two quick lookups first and full scan last
    var header = this.$$respHeaders[name];
    if (header) return header;

    name = angular.lowercase(name);
    header = this.$$respHeaders[name];
    if (header) return header;

    header = undefined;
    angular.forEach(this.$$respHeaders, function(headerVal, headerName) {
      if (!header && angular.lowercase(headerName) == name) header = headerVal;
    });
    return header;
  };

  this.getAllResponseHeaders = function() {
    var lines = [];

    angular.forEach(this.$$respHeaders, function(value, key) {
      lines.push(key + ': ' + value);
    });
    return lines.join('\n');
  };

  this.abort = angular.noop;
}


/**
 * @ngdoc service
 * @name $timeout
 * @description
 *
 * This service is just a simple decorator for {@link ng.$timeout $timeout} service
 * that adds a "flush" and "verifyNoPendingTasks" methods.
 */

angular.mock.$TimeoutDecorator = ['$delegate', '$browser', function($delegate, $browser) {

  /**
   * @ngdoc method
   * @name $timeout#flush
   * @description
   *
   * Flushes the queue of pending tasks.
   *
   * @param {number=} delay maximum timeout amount to flush up until
   */
  $delegate.flush = function(delay) {
    $browser.defer.flush(delay);
  };

  /**
   * @ngdoc method
   * @name $timeout#verifyNoPendingTasks
   * @description
   *
   * Verifies that there are no pending tasks that need to be flushed.
   */
  $delegate.verifyNoPendingTasks = function() {
    if ($browser.deferredFns.length) {
      throw new Error('Deferred tasks to flush (' + $browser.deferredFns.length + '): ' +
          formatPendingTasksAsString($browser.deferredFns));
    }
  };

  function formatPendingTasksAsString(tasks) {
    var result = [];
    angular.forEach(tasks, function(task) {
      result.push('{id: ' + task.id + ', ' + 'time: ' + task.time + '}');
    });

    return result.join(', ');
  }

  return $delegate;
}];

angular.mock.$RAFDecorator = ['$delegate', function($delegate) {
  var queue = [];
  var rafFn = function(fn) {
    var index = queue.length;
    queue.push(fn);
    return function() {
      queue.splice(index, 1);
    };
  };

  rafFn.supported = $delegate.supported;

  rafFn.flush = function() {
    if (queue.length === 0) {
      throw new Error('No rAF callbacks present');
    }

    var length = queue.length;
    for (var i = 0; i < length; i++) {
      queue[i]();
    }

    queue = [];
  };

  return rafFn;
}];

angular.mock.$AsyncCallbackDecorator = ['$delegate', function($delegate) {
  var callbacks = [];
  var addFn = function(fn) {
    callbacks.push(fn);
  };
  addFn.flush = function() {
    angular.forEach(callbacks, function(fn) {
      fn();
    });
    callbacks = [];
  };
  return addFn;
}];

/**
 *
 */
angular.mock.$RootElementProvider = function() {
  this.$get = function() {
    return angular.element('<div ng-app></div>');
  };
};

/**
 * @ngdoc service
 * @name $controller
 * @description
 * A decorator for {@link ng.$controller} with additional `bindings` parameter, useful when testing
 * controllers of directives that use {@link $compile#-bindtocontroller- `bindToController`}.
 *
 *
 * ## Example
 *
 * ```js
 *
 * // Directive definition ...
 *
 * myMod.directive('myDirective', {
 *   controller: 'MyDirectiveController',
 *   bindToController: {
 *     name: '@'
 *   }
 * });
 *
 *
 * // Controller definition ...
 *
 * myMod.controller('MyDirectiveController', ['log', function($log) {
 *   $log.info(this.name);
 * })];
 *
 *
 * // In a test ...
 *
 * describe('myDirectiveController', function() {
 *   it('should write the bound name to the log', inject(function($controller, $log) {
 *     var ctrl = $controller('MyDirective', { /* no locals &#42;/ }, { name: 'Clark Kent' });
 *     expect(ctrl.name).toEqual('Clark Kent');
 *     expect($log.info.logs).toEqual(['Clark Kent']);
 *   });
 * });
 *
 * ```
 *
 * @param {Function|string} constructor If called with a function then it's considered to be the
 *    controller constructor function. Otherwise it's considered to be a string which is used
 *    to retrieve the controller constructor using the following steps:
 *
 *    * check if a controller with given name is registered via `$controllerProvider`
 *    * check if evaluating the string on the current scope returns a constructor
 *    * if $controllerProvider#allowGlobals, check `window[constructor]` on the global
 *      `window` object (not recommended)
 *
 *    The string can use the `controller as property` syntax, where the controller instance is published
 *    as the specified property on the `scope`; the `scope` must be injected into `locals` param for this
 *    to work correctly.
 *
 * @param {Object} locals Injection locals for Controller.
 * @param {Object=} bindings Properties to add to the controller before invoking the constructor. This is used
 *                           to simulate the `bindToController` feature and simplify certain kinds of tests.
 * @return {Object} Instance of given controller.
 */
angular.mock.$ControllerDecorator = ['$delegate', function($delegate) {
  return function(expression, locals, later, ident) {
    if (later && typeof later === 'object') {
      var create = $delegate(expression, locals, true, ident);
      angular.extend(create.instance, later);
      return create();
    }
    return $delegate(expression, locals, later, ident);
  };
}];


/**
 * @ngdoc module
 * @name ngMock
 * @packageName angular-mocks
 * @description
 *
 * # ngMock
 *
 * The `ngMock` module provides support to inject and mock Angular services into unit tests.
 * In addition, ngMock also extends various core ng services such that they can be
 * inspected and controlled in a synchronous manner within test code.
 *
 *
 * <div doc-module-components="ngMock"></div>
 *
 */
angular.module('ngMock', ['ng']).provider({
  $browser: angular.mock.$BrowserProvider,
  $exceptionHandler: angular.mock.$ExceptionHandlerProvider,
  $log: angular.mock.$LogProvider,
  $interval: angular.mock.$IntervalProvider,
  $httpBackend: angular.mock.$HttpBackendProvider,
  $rootElement: angular.mock.$RootElementProvider
}).config(['$provide', function($provide) {
  $provide.decorator('$timeout', angular.mock.$TimeoutDecorator);
  $provide.decorator('$$rAF', angular.mock.$RAFDecorator);
  $provide.decorator('$$asyncCallback', angular.mock.$AsyncCallbackDecorator);
  $provide.decorator('$rootScope', angular.mock.$RootScopeDecorator);
  $provide.decorator('$controller', angular.mock.$ControllerDecorator);
}]);

/**
 * @ngdoc module
 * @name ngMockE2E
 * @module ngMockE2E
 * @packageName angular-mocks
 * @description
 *
 * The `ngMockE2E` is an angular module which contains mocks suitable for end-to-end testing.
 * Currently there is only one mock present in this module -
 * the {@link ngMockE2E.$httpBackend e2e $httpBackend} mock.
 */
angular.module('ngMockE2E', ['ng']).config(['$provide', function($provide) {
  $provide.decorator('$httpBackend', angular.mock.e2e.$httpBackendDecorator);
}]);

/**
 * @ngdoc service
 * @name $httpBackend
 * @module ngMockE2E
 * @description
 * Fake HTTP backend implementation suitable for end-to-end testing or backend-less development of
 * applications that use the {@link ng.$http $http service}.
 *
 * *Note*: For fake http backend implementation suitable for unit testing please see
 * {@link ngMock.$httpBackend unit-testing $httpBackend mock}.
 *
 * This implementation can be used to respond with static or dynamic responses via the `when` api
 * and its shortcuts (`whenGET`, `whenPOST`, etc) and optionally pass through requests to the
 * real $httpBackend for specific requests (e.g. to interact with certain remote apis or to fetch
 * templates from a webserver).
 *
 * As opposed to unit-testing, in an end-to-end testing scenario or in scenario when an application
 * is being developed with the real backend api replaced with a mock, it is often desirable for
 * certain category of requests to bypass the mock and issue a real http request (e.g. to fetch
 * templates or static files from the webserver). To configure the backend with this behavior
 * use the `passThrough` request handler of `when` instead of `respond`.
 *
 * Additionally, we don't want to manually have to flush mocked out requests like we do during unit
 * testing. For this reason the e2e $httpBackend flushes mocked out requests
 * automatically, closely simulating the behavior of the XMLHttpRequest object.
 *
 * To setup the application to run with this http backend, you have to create a module that depends
 * on the `ngMockE2E` and your application modules and defines the fake backend:
 *
 * ```js
 *   myAppDev = angular.module('myAppDev', ['myApp', 'ngMockE2E']);
 *   myAppDev.run(function($httpBackend) {
 *     phones = [{name: 'phone1'}, {name: 'phone2'}];
 *
 *     // returns the current list of phones
 *     $httpBackend.whenGET('/phones').respond(phones);
 *
 *     // adds a new phone to the phones array
 *     $httpBackend.whenPOST('/phones').respond(function(method, url, data) {
 *       var phone = angular.fromJson(data);
 *       phones.push(phone);
 *       return [200, phone, {}];
 *     });
 *     $httpBackend.whenGET(/^\/templates\//).passThrough();
 *     //...
 *   });
 * ```
 *
 * Afterwards, bootstrap your app with this new module.
 */

/**
 * @ngdoc method
 * @name $httpBackend#when
 * @module ngMockE2E
 * @description
 * Creates a new backend definition.
 *
 * @param {string} method HTTP method.
 * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
 *   and returns true if the url match the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
 *   object and returns true if the headers match the current definition.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 *
 *  - respond –
 *    `{function([status,] data[, headers, statusText])
 *    | function(function(method, url, data, headers)}`
 *    – The respond method takes a set of static data to be returned or a function that can return
 *    an array containing response status (number), response data (string), response headers
 *    (Object), and the text for the status (string).
 *  - passThrough – `{function()}` – Any request matching a backend definition with
 *    `passThrough` handler will be passed through to the real backend (an XHR request will be made
 *    to the server.)
 *  - Both methods return the `requestHandler` object for possible overrides.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenGET
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for GET requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
 *   and returns true if the url match the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenHEAD
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for HEAD requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
 *   and returns true if the url match the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenDELETE
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for DELETE requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
 *   and returns true if the url match the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPOST
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for POST requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
 *   and returns true if the url match the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPUT
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for PUT requests.  For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
 *   and returns true if the url match the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPATCH
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for PATCH requests.  For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
 *   and returns true if the url match the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenJSONP
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for JSONP requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives the url
 *   and returns true if the url match the current definition.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */
angular.mock.e2e = {};
angular.mock.e2e.$httpBackendDecorator =
  ['$rootScope', '$timeout', '$delegate', '$browser', createHttpBackendMock];


/**
 * @ngdoc type
 * @name $rootScope.Scope
 * @module ngMock
 * @description
 * {@link ng.$rootScope.Scope Scope} type decorated with helper methods useful for testing. These
 * methods are automatically available on any {@link ng.$rootScope.Scope Scope} instance when
 * `ngMock` module is loaded.
 *
 * In addition to all the regular `Scope` methods, the following helper methods are available:
 */
angular.mock.$RootScopeDecorator = ['$delegate', function($delegate) {

  var $rootScopePrototype = Object.getPrototypeOf($delegate);

  $rootScopePrototype.$countChildScopes = countChildScopes;
  $rootScopePrototype.$countWatchers = countWatchers;

  return $delegate;

  // ------------------------------------------------------------------------------------------ //

  /**
   * @ngdoc method
   * @name $rootScope.Scope#$countChildScopes
   * @module ngMock
   * @description
   * Counts all the direct and indirect child scopes of the current scope.
   *
   * The current scope is excluded from the count. The count includes all isolate child scopes.
   *
   * @returns {number} Total number of child scopes.
   */
  function countChildScopes() {
    // jshint validthis: true
    var count = 0; // exclude the current scope
    var pendingChildHeads = [this.$$childHead];
    var currentScope;

    while (pendingChildHeads.length) {
      currentScope = pendingChildHeads.shift();

      while (currentScope) {
        count += 1;
        pendingChildHeads.push(currentScope.$$childHead);
        currentScope = currentScope.$$nextSibling;
      }
    }

    return count;
  }


  /**
   * @ngdoc method
   * @name $rootScope.Scope#$countWatchers
   * @module ngMock
   * @description
   * Counts all the watchers of direct and indirect child scopes of the current scope.
   *
   * The watchers of the current scope are included in the count and so are all the watchers of
   * isolate child scopes.
   *
   * @returns {number} Total number of watchers.
   */
  function countWatchers() {
    // jshint validthis: true
    var count = this.$$watchers ? this.$$watchers.length : 0; // include the current scope
    var pendingChildHeads = [this.$$childHead];
    var currentScope;

    while (pendingChildHeads.length) {
      currentScope = pendingChildHeads.shift();

      while (currentScope) {
        count += currentScope.$$watchers ? currentScope.$$watchers.length : 0;
        pendingChildHeads.push(currentScope.$$childHead);
        currentScope = currentScope.$$nextSibling;
      }
    }

    return count;
  }
}];


if (window.jasmine || window.mocha) {

  var currentSpec = null,
      annotatedFunctions = [],
      isSpecRunning = function() {
        return !!currentSpec;
      };

  angular.mock.$$annotate = angular.injector.$$annotate;
  angular.injector.$$annotate = function(fn) {
    if (typeof fn === 'function' && !fn.$inject) {
      annotatedFunctions.push(fn);
    }
    return angular.mock.$$annotate.apply(this, arguments);
  };


  (window.beforeEach || window.setup)(function() {
    annotatedFunctions = [];
    currentSpec = this;
  });

  (window.afterEach || window.teardown)(function() {
    var injector = currentSpec.$injector;

    annotatedFunctions.forEach(function(fn) {
      delete fn.$inject;
    });

    angular.forEach(currentSpec.$modules, function(module) {
      if (module && module.$$hashKey) {
        module.$$hashKey = undefined;
      }
    });

    currentSpec.$injector = null;
    currentSpec.$modules = null;
    currentSpec = null;

    if (injector) {
      injector.get('$rootElement').off();
      var $browser = injector.get('$browser');
      if ($browser.pollFns) $browser.pollFns.length = 0;
    }

    // clean up jquery's fragment cache
    angular.forEach(angular.element.fragments, function(val, key) {
      delete angular.element.fragments[key];
    });

    MockXhr.$$lastInstance = null;

    angular.forEach(angular.callbacks, function(val, key) {
      delete angular.callbacks[key];
    });
    angular.callbacks.counter = 0;
  });

  /**
   * @ngdoc function
   * @name angular.mock.module
   * @description
   *
   * *NOTE*: This function is also published on window for easy access.<br>
   * *NOTE*: This function is declared ONLY WHEN running tests with jasmine or mocha
   *
   * This function registers a module configuration code. It collects the configuration information
   * which will be used when the injector is created by {@link angular.mock.inject inject}.
   *
   * See {@link angular.mock.inject inject} for usage example
   *
   * @param {...(string|Function|Object)} fns any number of modules which are represented as string
   *        aliases or as anonymous module initialization functions. The modules are used to
   *        configure the injector. The 'ng' and 'ngMock' modules are automatically loaded. If an
   *        object literal is passed they will be registered as values in the module, the key being
   *        the module name and the value being what is returned.
   */
  window.module = angular.mock.module = function() {
    var moduleFns = Array.prototype.slice.call(arguments, 0);
    return isSpecRunning() ? workFn() : workFn;
    /////////////////////
    function workFn() {
      if (currentSpec.$injector) {
        throw new Error('Injector already created, can not register a module!');
      } else {
        var modules = currentSpec.$modules || (currentSpec.$modules = []);
        angular.forEach(moduleFns, function(module) {
          if (angular.isObject(module) && !angular.isArray(module)) {
            modules.push(function($provide) {
              angular.forEach(module, function(value, key) {
                $provide.value(key, value);
              });
            });
          } else {
            modules.push(module);
          }
        });
      }
    }
  };

  /**
   * @ngdoc function
   * @name angular.mock.inject
   * @description
   *
   * *NOTE*: This function is also published on window for easy access.<br>
   * *NOTE*: This function is declared ONLY WHEN running tests with jasmine or mocha
   *
   * The inject function wraps a function into an injectable function. The inject() creates new
   * instance of {@link auto.$injector $injector} per test, which is then used for
   * resolving references.
   *
   *
   * ## Resolving References (Underscore Wrapping)
   * Often, we would like to inject a reference once, in a `beforeEach()` block and reuse this
   * in multiple `it()` clauses. To be able to do this we must assign the reference to a variable
   * that is declared in the scope of the `describe()` block. Since we would, most likely, want
   * the variable to have the same name of the reference we have a problem, since the parameter
   * to the `inject()` function would hide the outer variable.
   *
   * To help with this, the injected parameters can, optionally, be enclosed with underscores.
   * These are ignored by the injector when the reference name is resolved.
   *
   * For example, the parameter `_myService_` would be resolved as the reference `myService`.
   * Since it is available in the function body as _myService_, we can then assign it to a variable
   * defined in an outer scope.
   *
   * ```
   * // Defined out reference variable outside
   * var myService;
   *
   * // Wrap the parameter in underscores
   * beforeEach( inject( function(_myService_){
   *   myService = _myService_;
   * }));
   *
   * // Use myService in a series of tests.
   * it('makes use of myService', function() {
   *   myService.doStuff();
   * });
   *
   * ```
   *
   * See also {@link angular.mock.module angular.mock.module}
   *
   * ## Example
   * Example of what a typical jasmine tests looks like with the inject method.
   * ```js
   *
   *   angular.module('myApplicationModule', [])
   *       .value('mode', 'app')
   *       .value('version', 'v1.0.1');
   *
   *
   *   describe('MyApp', function() {
   *
   *     // You need to load modules that you want to test,
   *     // it loads only the "ng" module by default.
   *     beforeEach(module('myApplicationModule'));
   *
   *
   *     // inject() is used to inject arguments of all given functions
   *     it('should provide a version', inject(function(mode, version) {
   *       expect(version).toEqual('v1.0.1');
   *       expect(mode).toEqual('app');
   *     }));
   *
   *
   *     // The inject and module method can also be used inside of the it or beforeEach
   *     it('should override a version and test the new version is injected', function() {
   *       // module() takes functions or strings (module aliases)
   *       module(function($provide) {
   *         $provide.value('version', 'overridden'); // override version here
   *       });
   *
   *       inject(function(version) {
   *         expect(version).toEqual('overridden');
   *       });
   *     });
   *   });
   *
   * ```
   *
   * @param {...Function} fns any number of functions which will be injected using the injector.
   */



  var ErrorAddingDeclarationLocationStack = function(e, errorForStack) {
    this.message = e.message;
    this.name = e.name;
    if (e.line) this.line = e.line;
    if (e.sourceId) this.sourceId = e.sourceId;
    if (e.stack && errorForStack)
      this.stack = e.stack + '\n' + errorForStack.stack;
    if (e.stackArray) this.stackArray = e.stackArray;
  };
  ErrorAddingDeclarationLocationStack.prototype.toString = Error.prototype.toString;

  window.inject = angular.mock.inject = function() {
    var blockFns = Array.prototype.slice.call(arguments, 0);
    var errorForStack = new Error('Declaration Location');
    return isSpecRunning() ? workFn.call(currentSpec) : workFn;
    /////////////////////
    function workFn() {
      var modules = currentSpec.$modules || [];
      var strictDi = !!currentSpec.$injectorStrict;
      modules.unshift('ngMock');
      modules.unshift('ng');
      var injector = currentSpec.$injector;
      if (!injector) {
        if (strictDi) {
          // If strictDi is enabled, annotate the providerInjector blocks
          angular.forEach(modules, function(moduleFn) {
            if (typeof moduleFn === "function") {
              angular.injector.$$annotate(moduleFn);
            }
          });
        }
        injector = currentSpec.$injector = angular.injector(modules, strictDi);
        currentSpec.$injectorStrict = strictDi;
      }
      for (var i = 0, ii = blockFns.length; i < ii; i++) {
        if (currentSpec.$injectorStrict) {
          // If the injector is strict / strictDi, and the spec wants to inject using automatic
          // annotation, then annotate the function here.
          injector.annotate(blockFns[i]);
        }
        try {
          /* jshint -W040 *//* Jasmine explicitly provides a `this` object when calling functions */
          injector.invoke(blockFns[i] || angular.noop, this);
          /* jshint +W040 */
        } catch (e) {
          if (e.stack && errorForStack) {
            throw new ErrorAddingDeclarationLocationStack(e, errorForStack);
          }
          throw e;
        } finally {
          errorForStack = null;
        }
      }
    }
  };


  angular.mock.inject.strictDi = function(value) {
    value = arguments.length ? !!value : true;
    return isSpecRunning() ? workFn() : workFn;

    function workFn() {
      if (value !== currentSpec.$injectorStrict) {
        if (currentSpec.$injector) {
          throw new Error('Injector already created, can not modify strict annotations');
        } else {
          currentSpec.$injectorStrict = value;
        }
      }
    }
  };
}


})(window, window.angular);

(function() {
  angular.module("app").constant("config", {
    title: "foo"
  });

}).call(this);

(function() {
  window.mockEventSource = function() {
    var mocked;
    mocked = function(url) {
      var EventSourceMock;
      EventSourceMock = (function() {
        function EventSourceMock(url) {
          this.url = url;
          this.readyState = 1;
          this.onEvent = {};
        }

        EventSourceMock.prototype.addEventListener = function(event, cb) {
          if (!this.onEvent.hasOwnProperty(event)) {
            this.onEvent[event] = [];
          }
          return this.onEvent[event].push(cb);
        };

        EventSourceMock.prototype.fakeEvent = function(eventtype, event) {
          var cb, _i, _len, _ref, _results;
          if (this.onEvent.hasOwnProperty(eventtype)) {
            _ref = this.onEvent[eventtype];
            _results = [];
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              cb = _ref[_i];
              _results.push(cb(event));
            }
            return _results;
          }
        };

        EventSourceMock.prototype.close = function() {
          return this.readyState = 2;
        };

        return EventSourceMock;

      })();
      return new EventSourceMock(url);
    };
    return beforeEach(module(function($provide) {
      $provide.value("EventSource", mocked);
      return null;
    }));
  };

}).call(this);

(function() {
  window.decorateHttpBackend = function($httpBackend) {
    var getNextId, ids;
    ids = {};
    getNextId = function(namespace) {
      if (!ids.hasOwnProperty(namespace)) {
        ids[namespace] = 0;
      }
      ids[namespace] += 1;
      return ids[namespace];
    };
    $httpBackend.epExample = function(ep) {
      var i, _i, _ref;
      ep = ep.split("/");
      for (i = _i = 0, _ref = ep.length - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
        if (ep[i].indexOf("n:") === 0) {
          ep[i] = "1";
        }
        if (ep[i].indexOf("i:") === 0) {
          ep[i] = "id";
        }
      }
      return ep.join("/");
    };
    $httpBackend.epRegexp = function(ep) {
      var i, _i, _ref;
      ep = ep.split("/");
      for (i = _i = 0, _ref = ep.length - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
        if (ep[i].indexOf("n:") === 0) {
          ep[i] = "\\d+";
        }
        if (ep[i].indexOf("i:") === 0) {
          ep[i] = "[a-zA-Z_-][a-zA-Z0-9_-]*";
        }
      }
      return RegExp("^" + ep.join("/") + "$");
    };
    $httpBackend.epLastPath = function(path) {
      var splitpath;
      splitpath = path.split("/");
      return splitpath[splitpath.length - 1];
    };
    $httpBackend.resetIds = function() {
      return ids = {};
    };
    $httpBackend.buildDataValue = function(ep, nItems) {
      var data, dataEp, hint, i, ret, valueFromBaseType, valueFromSpec, _i, _j, _len, _ref, _ref1;
      valueFromBaseType = function(spec, hint) {
        var type;
        if (spec.hasOwnProperty("fields")) {
          return valueFromSpec(spec, hint);
        }
        if (hint == null) {
          hint = "mystring";
        }
        if (spec.name == null) {
          throw Error("no type: " + (JSON.stringify(spec)) + " " + hint);
        }
        type = spec.name;
        switch (type) {
          case "string":
            return hint;
          case "binary":
            return hint;
          case "identifier":
            return hint + getNextId(hint);
          case "integer":
            return getNextId(hint);
          case "boolean":
            return false;
          case "jsonobject":
            return {};
          case "link":
            return "http://link/link";
          case "datetime":
            return getNextId(hint);
          case "sourced-properties":
            return {
              prop: ['value', "source"]
            };
          default:
            throw Error("unknown type: " + type);
        }
      };
      valueFromSpec = function(spec, basehint) {
        var field, hint, ret, _i, _len, _ref;
        ret = {};
        _ref = spec.fields;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          field = _ref[_i];
          hint = "my" + field.name;
          if (field.name === "name") {
            hint = basehint;
          }
          if (field.type === "list") {
            ret[field.name] = [valueFromBaseType(field.type_spec.of, hint)];
          } else {
            ret[field.name] = valueFromBaseType(field.type_spec, hint);
          }
        }
        return ret;
      };
      hint = $httpBackend.epLastPath(ep).replace("n:", "");
      window.FIXTURES.dataspec = window.FIXTURES['dataspec.fixture.json'];
      if (window.FIXTURES.dataspec == null) {
        throw Error("dataspec is not available in test environment?!");
      }
      _ref = window.FIXTURES.dataspec;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        dataEp = _ref[_i];
        if (dataEp.re == null) {
          dataEp.re = this.epRegexp(dataEp.path);
        }
        if (dataEp.re.test(ep)) {
          if (nItems != null) {
            data = [];
            for (i = _j = 0, _ref1 = nItems - 1; _j <= _ref1; i = _j += 1) {
              data.push(valueFromBaseType(dataEp.type_spec, hint));
            }
          } else {
            data = [valueFromBaseType(dataEp.type_spec, hint)];
          }
          ret = {
            meta: {
              links: []
            }
          };
          ret[dataEp.plural] = data;
          return ret;
        }
      }
      throw Error("endpoint not specified! " + ep);
    };
    $httpBackend.whenDataGET = function(ep, opts) {
      if (opts == null) {
        opts = {};
      }
      opts.when = true;
      return this.expectDataGET(ep, opts);
    };
    return $httpBackend.expectDataGET = function(ep, opts) {
      var ep_query, value;
      if (opts == null) {
        opts = {
          nItems: void 0,
          override: void 0,
          when: void 0
        };
      }
      ep_query = ep.split("?");
      value = this.buildDataValue(this.epExample(ep_query[0]), opts.nItems);
      if (opts.override != null) {
        opts.override(value);
      }
      if (opts.when != null) {
        this.whenGET(this.epRegexp("api/v2/" + ep)).respond(value);
      } else {
        this.expectGET("api/v2/" + ep).respond(value);
      }
      return null;
    };
  };

  if (window.describe != null) {
    describe('decorateHttpBackend', function() {
      var $httpBackend, injected;
      $httpBackend = {};
      injected = function($injector) {
        $httpBackend = $injector.get('$httpBackend');
        return decorateHttpBackend($httpBackend);
      };
      beforeEach(inject(injected));
      it('should have correct endpoint matcher', function() {
        var epMatch;
        epMatch = function(a, b) {
          var re;
          re = $httpBackend.epRegexp(a);
          return re.test(b);
        };
        expect(epMatch("change", "change")).toBe(true);
        expect(epMatch("change/n:foo", "change/1")).toBe(true);
        expect(epMatch("change/n:foo", "change/sd")).toBe(false);
        expect(epMatch("change/foo/bar/n:foobar/foo", "change/foo/bar/1/foo")).toBe(true);
        return expect(epMatch("change/foo/bar/n:foobar/foo", "change/foo/bar/1/foo/")).toBe(false);
      });
      it('should have correct value builder for change', function() {
        var expected, i, k, v, value, _i, _ref, _results;
        expected = {
          files: ['myfiles'],
          category: 'mycategory',
          parent_changeids: [1],
          repository: 'myrepository',
          author: 'myauthor',
          project: 'myproject',
          comments: 'mycomments',
          changeid: 1,
          codebase: 'mycodebase',
          branch: 'mybranch',
          sourcestamp: {
            codebase: 'mycodebase',
            ssid: 1,
            repository: 'myrepository',
            created_at: 1,
            patch: {
              body: 'mybody',
              comment: 'mycomment',
              patchid: 1,
              level: 1,
              author: 'myauthor',
              subdir: 'mysubdir'
            },
            project: 'myproject',
            branch: 'mybranch',
            revision: 'myrevision'
          },
          revision: 'myrevision',
          revlink: 'myrevlink',
          properties: {
            'prop': ['value', 'source']
          },
          when_timestamp: 1
        };
        value = $httpBackend.buildDataValue("changes").changes[0];
        for (k in value) {
          v = value[k];
          expect(v).toEqual(expected[k]);
        }
        $httpBackend.resetIds();
        value = $httpBackend.buildDataValue("changes", 2).changes;
        expected = [expected, JSON.parse(JSON.stringify(expected).replace(/1/g, "2"))];
        expect(value.length).toEqual(expected.length);
        _results = [];
        for (i = _i = 0, _ref = value.length - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
          _results.push(expect(value[i]).toEqual(expected[i]));
        }
        return _results;
      });
      return it('should have value builder not crash for all data spec cases', function() {
        var dataEp, _i, _len, _ref, _results;
        _ref = window.FIXTURES.dataspec;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          dataEp = _ref[_i];
          _results.push($httpBackend.buildDataValue($httpBackend.epExample(dataEp.path)));
        }
        return _results;
      });
    });
  }

}).call(this);

(function() {
  var __slice = [].slice;

  beforeEach(module('app'));

  describe('buildrequest controller', function() {
    var $httpBackend, $rootScope, $scope, $stateParams, $timeout, buildbotService, createController, goneto, injected, mqService;
    buildbotService = mqService = $scope = $httpBackend = $rootScope = null;
    $timeout = createController = $stateParams = null;
    goneto = null;
    beforeEach(module(function($provide) {
      $provide.value("$state", {
        go: function() {
          var args;
          args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
          return goneto = args;
        }
      });
      $provide.value("$stateParams", {
        buildrequest: 1
      });
      return null;
    }));
    injected = function($injector) {
      var $controller, $q;
      $httpBackend = $injector.get('$httpBackend');
      decorateHttpBackend($httpBackend);
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      mqService = $injector.get('mqService');
      $timeout = $injector.get('$timeout');
      $stateParams = $injector.get('$stateParams');
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      spyOn(mqService, "setBaseUrl").and.returnValue(null);
      spyOn(mqService, "startConsuming").and.returnValue($q.when(function() {}));
      spyOn(mqService, "stopConsuming").and.returnValue(null);
      buildbotService = $injector.get('buildbotService');
      createController = function() {
        return $controller('buildrequestController', {
          $scope: $scope
        });
      };
      $httpBackend.expectDataGET('buildrequests/1');
      $httpBackend.expectDataGET('builders/1');
      return $httpBackend.expectDataGET('buildsets/1');
    };
    beforeEach(inject(injected));
    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      return $httpBackend.verifyNoOutstandingRequest();
    });
    it('should query for buildrequest', function() {
      var controller;
      controller = createController();
      $httpBackend.flush();
      $scope.buildrequest.claimed = true;
      $httpBackend.expectDataGET('builds?buildrequestid=1');
      $httpBackend.flush();
      expect($scope.builds[0].buildid).toBeDefined();
      $timeout.flush();
      return $httpBackend.verifyNoOutstandingRequest();
    });
    it('should query for builds again if first query returns 0', function() {
      var controller;
      controller = createController();
      $httpBackend.flush();
      $scope.buildrequest.claimed = true;
      $httpBackend.expectDataGET('builds?buildrequestid=1', {
        nItems: 0
      });
      $httpBackend.flush();
      expect($scope.builds.length).toBe(0);
      $httpBackend.expectDataGET('builds?buildrequestid=1', {
        nItems: 0
      });
      $timeout.flush();
      $httpBackend.flush();
      expect($scope.builds.length).toBe(0);
      $httpBackend.expectDataGET('builds?buildrequestid=1', {
        nItems: 1
      });
      $timeout.flush();
      $httpBackend.flush();
      expect($scope.builds[0].buildid).toBeDefined();
      $timeout.flush();
      return $httpBackend.verifyNoOutstandingRequest();
    });
    return it('should go to build page if build started', function() {
      var controller;
      $stateParams.redirect_to_build = 1;
      controller = createController();
      $httpBackend.flush();
      $scope.buildrequest.claimed = true;
      $httpBackend.expectDataGET('builds?buildrequestid=1', {
        nItems: 0
      });
      $httpBackend.flush();
      expect($scope.builds.length).toBe(0);
      $httpBackend.expectDataGET('builds?buildrequestid=1', {
        nItems: 1
      });
      $timeout.flush();
      $httpBackend.flush();
      expect($scope.builds[0].buildid).toBeDefined();
      $timeout.flush();
      $httpBackend.verifyNoOutstandingRequest();
      return expect(goneto).toEqual([
        'build', {
          builder: 3,
          build: 1
        }
      ]);
    });
  });

}).call(this);

(function() {
  describe('page with sidebar', function() {
    var assertDOM, elements, elmBody, padding, printDOM, queries, rootScope, scope, scrollTo, timeout;
    beforeEach(module("app"));
    elmBody = scope = rootScope = queries = timeout = null;
    padding = function(pix) {
      return {
        type: "padding",
        height: pix
      };
    };
    elements = function(start, end) {
      return {
        type: "elements",
        start: start,
        end: end
      };
    };
    assertDOM = function(l) {
      var c, childs, i, item, _i, _len, _results;
      childs = [];
      $("div", elmBody).each(function(i, c) {
        return childs.push(c);
      });
      _results = [];
      for (_i = 0, _len = l.length; _i < _len; _i++) {
        item = l[_i];
        if (item.type === "padding") {
          c = childs.shift();
          expect($(c).hasClass("padding")).toBe(true, c.outerHTML);
          expect($(c).height()).toEqual(item.height, c.outerHTML);
        }
        if (item.type === "elements") {
          _results.push((function() {
            var _j, _ref, _ref1, _results1;
            _results1 = [];
            for (i = _j = _ref = item.start, _ref1 = item.end; _ref <= _ref1 ? _j <= _ref1 : _j >= _ref1; i = _ref <= _ref1 ? ++_j : --_j) {
              c = childs.shift();
              expect($(c).hasClass("padding")).toBe(false, c.outerHTML);
              _results1.push(expect(c.innerText).toEqual(i.toString() + "a" + i.toString(), c.outerHTML));
            }
            return _results1;
          })());
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    };
    printDOM = function() {
      return $("div", elmBody).each(function() {
        if ($(this).hasClass("padding")) {
          return console.log("padding", $(this).height());
        } else {
          return console.log("row", this.innerText, $(this).height());
        }
      });
    };
    scrollTo = function(pos, verifyPos) {
      if (verifyPos == null) {
        verifyPos = pos;
      }
      elmBody.scrollTop(pos);
      expect(elmBody.scrollTop()).toBe(verifyPos);
      elmBody.trigger("scroll");
      timeout.flush();
      return expect(elmBody.scrollTop()).toBe(verifyPos);
    };
    beforeEach(inject(function($rootScope, $compile, glMenuService, $timeout, $q, $document) {
      timeout = $timeout;
      queries = [];
      rootScope = $rootScope;
      elmBody = angular.element('<div scroll-viewport style="height:50px">' + '<div style="height:10px" total-size="1000" scroll="item in items">{{::$index}}a{{::item.v}}' + '</div></div>');
      scope = $rootScope.$new();
      scope.items = {
        get: function(index, num) {
          var d;
          queries.push([index, num]);
          d = $q.defer();
          $timeout(function() {
            var i, ret, _i, _ref;
            ret = [];
            for (i = _i = 0, _ref = num - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
              ret.push({
                v: index + i
              });
            }
            return d.resolve(ret);
          });
          return d.promise;
        }
      };
      $compile(elmBody)(scope)[0];
      scope.$digest();
      return elmBody.appendTo("body");
    }));
    it('should initially load 2 screens', inject(function($timeout) {
      $timeout.flush();
      expect(queries).toEqual([[0, 10]]);
      assertDOM([elements(0, 9), padding(9900)]);
      return expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
    }));
    it('if scroll to middle, should load 3 screens', inject(function($timeout) {
      $timeout.flush();
      scrollTo(600);
      expect(queries).toEqual([[0, 10], [55, 15]]);
      assertDOM([elements(0, 9), padding(450), elements(55, 69), padding(10000 - 700)]);
      return expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
    }));
    it('several scroll loads several screens, and paddings are cleaned out', inject(function($timeout) {
      $timeout.flush();
      scrollTo(600);
      expect(queries).toEqual([[0, 10], [55, 15]]);
      assertDOM([elements(0, 9), padding(450), elements(55, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(400);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15]]);
      assertDOM([elements(0, 9), padding(250), elements(35, 49), padding(50), elements(55, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(500);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15], [50, 5]]);
      assertDOM([elements(0, 9), padding(250), elements(35, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(100);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15], [50, 5], [10, 10]]);
      assertDOM([elements(0, 19), padding(150), elements(35, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(200);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15], [50, 5], [10, 10], [20, 10]]);
      assertDOM([elements(0, 29), padding(50), elements(35, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(300);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15], [50, 5], [10, 10], [20, 10], [30, 5]]);
      assertDOM([elements(0, 69), padding(10000 - 700)]);
      return expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
    }));
    return it('Scroll to the end', inject(function($timeout) {
      $timeout.flush();
      scrollTo(10000, 9950);
      expect(queries).toEqual([[0, 10], [990, 10]]);
      return assertDOM([elements(0, 9), padding(9800), elements(990, 999)]);
    }));
  });

}).call(this);

(function() {
  var __slice = [].slice;

  beforeEach(module('app'));

  describe('buildrequest summary controller', function() {
    var $httpBackend, $rootScope, $scope, $timeout, buildbotService, createController, goneto, injected, mqService;
    buildbotService = mqService = $scope = $httpBackend = $rootScope = null;
    $timeout = createController = null;
    goneto = null;
    beforeEach(module(function($provide) {
      $provide.value("$state", {
        go: function() {
          var args;
          args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
          return goneto = args;
        }
      });
      return null;
    }));
    injected = function($injector) {
      var $controller, $q;
      $httpBackend = $injector.get('$httpBackend');
      decorateHttpBackend($httpBackend);
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $scope.buildrequestid = 1;
      mqService = $injector.get('mqService');
      $timeout = $injector.get('$timeout');
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      spyOn(mqService, "setBaseUrl").and.returnValue(null);
      spyOn(mqService, "startConsuming").and.returnValue($q.when(function() {}));
      spyOn(mqService, "stopConsuming").and.returnValue(null);
      buildbotService = $injector.get('buildbotService');
      return createController = function() {
        return $controller('_buildrequestsummaryController', {
          $scope: $scope
        });
      };
    };
    beforeEach(inject(injected));
    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      return $httpBackend.verifyNoOutstandingRequest();
    });
    it('should query for buildrequest', function() {
      var controller;
      $httpBackend.expectDataGET('buildrequests/1');
      controller = createController();
      $httpBackend.flush();
      $scope.buildrequest.claimed = true;
      $httpBackend.expectDataGET('builds?buildrequestid=1');
      $httpBackend.flush();
      expect($scope.builds[0].buildid).toBeDefined();
      $timeout.flush();
      return $httpBackend.verifyNoOutstandingRequest();
    });
    return it('should query for builds again if first query returns 0', function() {
      var controller;
      $httpBackend.expectDataGET('buildrequests/1');
      controller = createController();
      $httpBackend.flush();
      $scope.buildrequest.claimed = true;
      $httpBackend.expectDataGET('builds?buildrequestid=1', {
        nItems: 0
      });
      $httpBackend.flush();
      expect($scope.builds.length).toBe(0);
      $httpBackend.expectDataGET('builds?buildrequestid=1', {
        nItems: 0
      });
      $timeout.flush();
      $httpBackend.flush();
      expect($scope.builds.length).toBe(0);
      $httpBackend.expectDataGET('builds?buildrequestid=1', {
        nItems: 1
      });
      $timeout.flush();
      $httpBackend.flush();
      expect($scope.builds[0].buildid).toBeDefined();
      $timeout.flush();
      return $httpBackend.verifyNoOutstandingRequest();
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('buildsticker controller', function() {
    var $compile, $httpBackend, $rootScope, buildbotService, injected, mqService, results;
    buildbotService = mqService = $httpBackend = $rootScope = $compile = results = null;
    injected = function($injector) {
      var $controller, $location, $q;
      $compile = $injector.get('$compile');
      $httpBackend = $injector.get('$httpBackend');
      $location = $injector.get('$location');
      decorateHttpBackend($httpBackend);
      $rootScope = $injector.get('$rootScope');
      mqService = $injector.get('mqService');
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      results = $injector.get('RESULTS');
      spyOn(mqService, "setBaseUrl").and.returnValue(null);
      spyOn(mqService, "startConsuming").and.returnValue($q.when(function() {}));
      spyOn(mqService, "stopConsuming").and.returnValue(null);
      return buildbotService = $injector.get('buildbotService');
    };
    beforeEach(inject(injected));
    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      return $httpBackend.verifyNoOutstandingRequest();
    });
    return it('directive should generate correct html', function() {
      var build, buildLink, durationSpan, element, resultSpan, row0, row1, startedSpan, stateSpan, sticker;
      $httpBackend.expectDataGET('builds/1');
      buildbotService.one('builds', 1).bind($rootScope);
      $httpBackend.flush();
      $httpBackend.expectDataGET('builders/1');
      element = $compile("<buildsticker build='build'></buildsticker>")($rootScope);
      $httpBackend.flush();
      $rootScope.$digest();
      build = $rootScope.build;
      sticker = element.children().eq(0);
      row0 = sticker.children().eq(0);
      row1 = sticker.children().eq(1);
      resultSpan = row0.children().eq(0);
      buildLink = row0.children().eq(1);
      durationSpan = row1.children().eq(0);
      startedSpan = row1.children().eq(1);
      stateSpan = row1.children().eq(2);
      expect(buildLink.attr('href')).toBe('#/builders/2/builds/1');
      build.complete = false;
      build.results = -1;
      build.state_string = 'pending';
      $rootScope.$digest();
      expect(resultSpan.hasClass('results_PENDING')).toBe(true);
      expect(resultSpan.text()).toBe('...');
      expect(durationSpan.hasClass('ng-hide')).toBe(true);
      expect(startedSpan.hasClass('ng-hide')).toBe(false);
      expect(stateSpan.text()).toBe('pending');
      build.complete = true;
      build.complete_at = 2;
      build.results = results.SUCCESS;
      build.state_string = 'finished';
      $rootScope.$digest();
      expect(resultSpan.hasClass('results_SUCCESS')).toBe(true);
      expect(resultSpan.text()).toBe('SUCCESS');
      expect(durationSpan.hasClass('ng-hide')).toBe(false);
      expect(startedSpan.hasClass('ng-hide')).toBe(true);
      expect(durationSpan.text()).toBe('1 s');
      expect(stateSpan.text()).toBe('finished');
      build.complete = true;
      build.complete_at = 2;
      build.results = results.FAILURE;
      build.state_string = 'failed';
      $rootScope.$digest();
      expect(resultSpan.hasClass('results_FAILURE')).toBe(true);
      expect(resultSpan.text()).toBe('FAILURE');
      expect(durationSpan.hasClass('ng-hide')).toBe(false);
      expect(startedSpan.hasClass('ng-hide')).toBe(true);
      expect(durationSpan.text()).toBe('1 s');
      return expect(stateSpan.text()).toBe('failed');
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('buildsummary controller', function() {
    var $httpBackend, $rootScope, $scope, $stateParams, $timeout, baseurl, buildbotService, createController, goneto, injected, mqService, results;
    buildbotService = mqService = $scope = $httpBackend = $rootScope = null;
    $timeout = createController = $stateParams = results = baseurl = null;
    goneto = null;
    injected = function($injector) {
      var $controller, $location, $q;
      $httpBackend = $injector.get('$httpBackend');
      $location = $injector.get('$location');
      decorateHttpBackend($httpBackend);
      results = $injector.get('RESULTS');
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $scope.buildid = 1;
      $scope.condensed = 0;
      $httpBackend.expectDataGET('builds/1');
      $httpBackend.expectDataGET('builders/1');
      $httpBackend.expectDataGET('builds/1/steps', {
        nChilds: 2
      });
      $httpBackend.expectDataGET('steps/1/logs', {
        nChilds: 2
      });
      mqService = $injector.get('mqService');
      $timeout = $injector.get('$timeout');
      $stateParams = $injector.get('$stateParams');
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      baseurl = $location.absUrl().split("#")[0];
      spyOn(mqService, "setBaseUrl").and.returnValue(null);
      spyOn(mqService, "startConsuming").and.returnValue($q.when(function() {}));
      spyOn(mqService, "stopConsuming").and.returnValue(null);
      buildbotService = $injector.get('buildbotService');
      return createController = function() {
        return $controller('_buildsummaryController', {
          '$scope': $scope
        });
      };
    };
    beforeEach(inject(injected));
    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      return $httpBackend.verifyNoOutstandingRequest();
    });
    it('should provide correct isStepDisplayed when condensed', function() {
      var controller;
      $scope.condensed = 1;
      controller = createController();
      $httpBackend.flush();
      expect($scope.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect($scope.isStepDisplayed({
        results: results.WARNING
      })).toBe(false);
      expect($scope.isStepDisplayed({
        results: results.FAILURE
      })).toBe(false);
      $scope.toggleDetails();
      expect($scope.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect($scope.isStepDisplayed({
        results: results.WARNING
      })).toBe(true);
      expect($scope.isStepDisplayed({
        results: results.FAILURE
      })).toBe(true);
      $scope.toggleDetails();
      expect($scope.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(true);
      expect($scope.isStepDisplayed({
        results: results.WARNING
      })).toBe(true);
      expect($scope.isStepDisplayed({
        results: results.FAILURE
      })).toBe(true);
      $scope.toggleDetails();
      expect($scope.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect($scope.isStepDisplayed({
        results: results.WARNING
      })).toBe(false);
      return expect($scope.isStepDisplayed({
        results: results.FAILURE
      })).toBe(false);
    });
    it('should provide correct isStepDisplayed when not condensed', function() {
      var controller;
      $scope.condensed = 0;
      controller = createController();
      $httpBackend.flush();
      expect($scope.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(true);
      expect($scope.isStepDisplayed({
        results: results.WARNING
      })).toBe(true);
      expect($scope.isStepDisplayed({
        results: results.FAILURE
      })).toBe(true);
      $scope.toggleDetails();
      expect($scope.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect($scope.isStepDisplayed({
        results: results.WARNING
      })).toBe(false);
      expect($scope.isStepDisplayed({
        results: results.FAILURE
      })).toBe(false);
      $scope.toggleDetails();
      expect($scope.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect($scope.isStepDisplayed({
        results: results.WARNING
      })).toBe(true);
      expect($scope.isStepDisplayed({
        results: results.FAILURE
      })).toBe(true);
      return $scope.toggleDetails();
    });
    it('should provide correct getBuildRequestIDFromURL', function() {
      var controller;
      controller = createController();
      $httpBackend.flush();
      return expect($scope.getBuildRequestIDFromURL("" + baseurl + "#buildrequests/123")).toBe(123);
    });
    it('should provide correct isBuildRequestURL', function() {
      var controller;
      controller = createController();
      $httpBackend.flush();
      expect($scope.isBuildRequestURL("" + baseurl + "#buildrequests/123")).toBe(true);
      expect($scope.isBuildRequestURL("http://otherdomain:5000/#buildrequests/123")).toBe(false);
      expect($scope.isBuildRequestURL("" + baseurl + "#builds/123")).toBe(false);
      return expect($scope.isBuildRequestURL("" + baseurl + "#buildrequests/bla")).toBe(false);
    });
    return it('should provide correct isBuildURL', function() {
      var controller;
      controller = createController();
      $httpBackend.flush();
      expect($scope.isBuildURL("" + baseurl + "#builders/123/builds/123")).toBe(true);
      return expect($scope.isBuildURL("" + baseurl + "#builders/sdf/builds/123")).toBe(false);
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('changelist controller', function() {
    var $rootScope, $scope, createController, injected;
    $scope = $rootScope = createController = null;
    injected = function($injector) {
      var $controller;
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $controller = $injector.get('$controller');
      return createController = function() {
        return $controller('_changeListController', {
          '$scope': $scope
        });
      };
    };
    beforeEach(inject(injected));
    return it('should calculate authors emails', function() {
      var controller;
      controller = createController();
      $scope.changes = [
        {
          author: "foo <bar@foo.com>"
        }, {
          author: "bar <foo@foo.com>"
        }
      ];
      $scope.$digest();
      expect($scope.changes[0].author_email).toBe("bar@foo.com");
      return expect($scope.changes[1].author_email).toBe("foo@foo.com");
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('buildbot service', function() {
    var $httpBackend, $rootScope, $scope, $timeout, buildbotService, injected, mqService;
    buildbotService = mqService = $scope = $httpBackend = $rootScope = $timeout = null;
    injected = function($injector) {
      var $q;
      $httpBackend = $injector.get('$httpBackend');
      decorateHttpBackend($httpBackend);
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      mqService = $injector.get('mqService');
      $timeout = $injector.get('$timeout');
      $q = $injector.get('$q');
      spyOn(mqService, "setBaseUrl").and.returnValue(null);
      spyOn(mqService, "startConsuming").and.returnValue($q.when(function() {}));
      spyOn(mqService, "stopConsuming").and.returnValue(null);
      return buildbotService = $injector.get('buildbotService');
    };
    beforeEach(inject(injected));
    it('should query for changes at /changes and receive an empty array', function() {
      $httpBackend.expectDataGET('changes', {
        nItems: 1
      });
      buildbotService.all("changes").bind($scope);
      $httpBackend.flush();
      return expect($scope.changes.length).toBe(1);
    });
    it('should query for builds/1/steps/2 and receive a SUCCESS result', function() {
      var r;
      $httpBackend.expectDataGET('builds/1/steps/2', {
        override: function(res) {
          return res.steps[0].res = "SUCCESS";
        }
      });
      r = buildbotService.one("builds", 1).one("steps", 2);
      r.bind($scope, {
        dest_key: "step_scope"
      });
      $httpBackend.flush();
      return expect($scope.step_scope.res).toBe("SUCCESS");
    });
    it('should query for builds/1/steps/2 mocked via dataspec', function() {
      var r;
      $httpBackend.expectDataGET('builds/1/steps/2');
      r = buildbotService.one("builds", 1).one("steps", 2);
      r.bind($scope);
      $httpBackend.flush();
      return expect($scope.step.state_string).toEqual("mystate_string");
    });
    it('should query default scope_key to route key', function() {
      $httpBackend.expectGET('api/v2/builds/1/steps/2').respond({
        steps: [
          {
            res: "SUCCESS"
          }
        ]
      });
      buildbotService.one("builds", 1).one("steps", 2).bind($scope);
      $httpBackend.flush();
      return expect($scope.step.res).toBe("SUCCESS");
    });
    it('should update the $scope when event received', function() {
      var r;
      $httpBackend.expectGET('api/v2/builds/1/steps/2').respond({
        steps: [
          {
            res: "PENDING",
            otherfield: "FOO"
          }
        ]
      });
      r = buildbotService.one("builds", 1).one("steps", 2);
      r.bind($scope, {
        ismutable: function() {
          return true;
        }
      });
      $httpBackend.flush();
      expect($scope.step.res).toBe("PENDING");
      mqService.broadcast("builds/1/steps/2/update", {
        "res": "SUCCESS"
      });
      $rootScope.$digest();
      expect($scope.step.res).toBe("SUCCESS");
      return expect($scope.step.otherfield).toBe("FOO");
    });
    it('should update the $scope when event received for collections', function() {
      var c, childs, r, _i, _len;
      $httpBackend.expectGET('api/v2/builds/1/steps').respond({
        steps: [
          {
            stepid: 1,
            res: "PENDING",
            otherfield: "FOO"
          }
        ]
      });
      r = buildbotService.one("builds", 1).all("steps");
      childs = [];
      r.bind($scope, {
        ismutable: function() {
          return true;
        },
        onchild: function(c) {
          return childs.push(c);
        }
      });
      $httpBackend.flush();
      expect($scope.steps.length).toBe(1);
      mqService.broadcast("builds/1/steps/3/new", {
        stepid: 3,
        "res": "SUCCESS"
      });
      $rootScope.$digest();
      expect($scope.steps.length).toBe(2);
      expect(childs.length).toBe(2);
      for (_i = 0, _len = childs.length; _i < _len; _i++) {
        c = childs[_i];
        expect(c.all).toBeDefined();
        expect(c.one).toBeDefined();
      }
      return expect($scope.steps[1].res).toBe("SUCCESS");
    });
    it('should update the $scope when event received for collections with same id', function() {
      var r;
      $httpBackend.expectGET('api/v2/builds/1/steps').respond({
        steps: [
          {
            stepid: 1,
            res: "PENDING",
            otherfield: "FOO"
          }
        ]
      });
      r = buildbotService.one("builds", 1).all("steps");
      r.bind($scope);
      $httpBackend.flush();
      expect($scope.steps.length).toBe(1);
      mqService.broadcast("builds/1/steps/3/new", {
        stepid: 3,
        "res": "SUCCESS"
      });
      mqService.broadcast("builds/1/steps/1/update", {
        stepid: 1,
        res: "SUCCESS"
      });
      $rootScope.$digest();
      expect($scope.steps.length).toBe(2);
      expect($scope.steps[0].res).toBe("SUCCESS");
      return expect($scope.steps[1].res).toBe("SUCCESS");
    });
    it('has a onchild api which should be usable for restangular api', function() {
      var r;
      $httpBackend.expectGET('api/v2/builds').respond({
        builds: [
          {
            buildid: 1,
            res: "PENDING",
            otherfield: "FOO"
          }
        ]
      });
      $httpBackend.expectDataGET('builds/1/steps');
      r = buildbotService.all("builds");
      r.bind($scope, {
        ismutable: function() {
          return true;
        },
        onchild: function(build) {
          return build.all("steps").bind($scope, {
            dest: build
          });
        }
      });
      $httpBackend.flush();
      $httpBackend.expectDataGET('builds/3/steps');
      mqService.broadcast("builds/3/new", {
        buildid: 3,
        "res": "SUCCESS"
      });
      $httpBackend.flush();
      expect($scope.builds[0].steps).toBeDefined();
      return expect($scope.builds[1].steps).toBeDefined();
    });
    it('has a bindHierarchy helper to bind a hierarchy', function() {
      var p, res;
      $httpBackend.expectDataGET('builds/1');
      $httpBackend.expectDataGET('builds/1/steps/2');
      p = buildbotService.bindHierarchy($scope, {
        build: 1,
        step: 2
      }, ["builds", "steps"]);
      res = null;
      p.then(function(r) {
        return res = r;
      });
      $httpBackend.flush();
      $rootScope.$digest();
      expect($scope.build).toBeDefined();
      expect($scope.step).toBeDefined();
      return expect([$scope.build, $scope.step]).toEqual(res);
    });
    it('should return the same object for several subsequent\ncalls to all(), one() and some()', function() {
      var r, r2, r3;
      r = buildbotService.all("build");
      r2 = buildbotService.all("build");
      expect(r).toBe(r2);
      r = buildbotService.one("build", 1);
      r2 = buildbotService.one("build", 1);
      r3 = buildbotService.one("build", 2);
      expect(r).toBe(r2);
      expect(r).not.toBe(r3);
      r = buildbotService.one("builder", 1).all("build");
      r2 = buildbotService.one("builder", 1).all("build");
      expect(r).toBe(r2);
      r = buildbotService.one("builder", 1).one("build", 1);
      r2 = buildbotService.one("builder", 1).one("build", 1);
      expect(r).toBe(r2);
      r = buildbotService.one("builder", 1).some("build", {
        limit: 20
      });
      r2 = buildbotService.one("builder", 1).some("build", {
        limit: 20
      });
      return expect(r).toBe(r2);
    });
    it('should use one request for one endpoint, take advantage of\nevents to maintain synchronisation', function() {
      var $scope2, builds1, builds2, r, r2;
      $httpBackend.expectDataGET('builds');
      r = buildbotService.all("builds");
      builds1 = [];
      r2 = buildbotService.all("builds");
      $scope2 = $rootScope.$new();
      builds2 = [];
      r.bind($scope, {
        onchild: function(build) {
          return builds1.push(build);
        }
      });
      r2.bind($scope2, {
        onchild: function(build) {
          return builds2.push(build);
        }
      });
      $httpBackend.flush();
      $rootScope.$digest();
      mqService.broadcast("builds/3/new", {
        buildid: 3,
        "res": "SUCCESS"
      });
      mqService.broadcast("builds/4/new", {
        buildid: 4,
        "res": "SUCCESS"
      });
      mqService.broadcast("builds/5/new", {
        buildid: 5,
        "res": "SUCCESS"
      });
      $rootScope.$digest();
      expect($scope.builds).toBe($scope2.builds);
      expect(builds1).not.toBe(builds2);
      expect(builds1[0]).toBe(builds2[0]);
      expect(builds1).toEqual(builds2);
      $scope.$destroy();
      $timeout.flush();
      mqService.broadcast("builds/6/new", {
        buildid: 6,
        "res": "SUCCESS"
      });
      $rootScope.$digest();
      expect(builds1.length + 1).toEqual(builds2.length);
      $scope2.$destroy();
      $timeout.flush();
      return expect(function() {
        return mqService.broadcast("builds/7/new", {
          buildid: 7,
          "res": "SUCCESS"
        });
      }).toThrow();
    });
    return it('should reload the data in case of loss of synchronisation', function() {
      var r;
      $httpBackend.expectDataGET('builds', {
        nItems: 1
      });
      r = buildbotService.all("builds");
      r.bind($scope);
      $httpBackend.flush();
      $rootScope.$digest();
      mqService.broadcast("builds/3/new", {
        buildid: 3,
        "res": "SUCCESS"
      });
      $rootScope.$digest();
      expect($scope.builds.length).toBe(2);
      $httpBackend.expectDataGET('builds', {
        nItems: 2
      });
      $rootScope.$broadcast("mq.restored_connection");
      $httpBackend.flush();
      $rootScope.$digest();
      expect($scope.builds.length).toBe(2);
      mqService.broadcast("builds/4/new", {
        buildid: 4,
        "res": "SUCCESS"
      });
      $rootScope.$digest();
      return expect($scope.builds.length).toBe(3);
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('mq service', function() {
    var $httpBackend, $rootScope, $scope, event_receiver, injected, mqService, ws;
    mqService = $scope = $httpBackend = $rootScope = null;
    ws = {
      send: function() {}
    };
    event_receiver = {
      receiver1: function() {},
      receiver2: function() {}
    };
    injected = function($injector) {
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      mqService = $injector.get('mqService');
      spyOn(mqService, "getWebSocket").and.returnValue(ws);
      spyOn(ws, "send").and.returnValue(null);
      spyOn(event_receiver, "receiver1").and.returnValue(null);
      return spyOn(event_receiver, "receiver2").and.returnValue(null);
    };
    beforeEach(inject(injected));
    it('match function should be correct', function() {
      expect(mqService._match("a/b/*", "a/b/c")).toBe(true);
      expect(mqService._match("a/b/*", "a/b/c/d")).toBe(false);
      expect(mqService._match("a/b/*/*", "a/b/c/d")).toBe(true);
      return expect(mqService._match("a/b/*/*", "a/b/c/d/e")).toBe(false);
    });
    it('should setup everything in setBaseURL', function() {
      expect(ws.onopen).toBeUndefined();
      mqService.setBaseUrl("ws");
      expect(mqService.getWebSocket).toHaveBeenCalled();
      expect(ws.onopen).toBeDefined();
      expect(ws.onerror).toBeDefined();
      return expect(ws.onmessage).toBeDefined();
    });
    it('should work with simple pub/sub usecase', function() {
      mqService.setBaseUrl("sse/");
      mqService.on("bla", event_receiver.receiver1);
      mqService.broadcast("bla", {
        "msg": true
      });
      return expect(event_receiver.receiver1).toHaveBeenCalledWith({
        "msg": true
      }, "bla");
    });
    it('should work with generic pub/sub usecase', function() {
      mqService.setBaseUrl("sse/");
      mqService.on("*/bla", event_receiver.receiver1);
      mqService.broadcast("1/bla", {
        "msg": true
      });
      expect(event_receiver.receiver1).toHaveBeenCalledWith({
        "msg": true
      }, "1/bla");
      mqService.broadcast("2/bla", {
        "msg": true
      });
      return expect(event_receiver.receiver1).toHaveBeenCalledWith({
        "msg": true
      }, "2/bla");
    });
    it('should send to several receivers', function() {
      mqService.setBaseUrl("sse/");
      mqService.on("1/bla", event_receiver.receiver1);
      mqService.on("*/bla", event_receiver.receiver2);
      mqService.broadcast("1/bla", {
        "msg": true
      });
      expect(event_receiver.receiver1).toHaveBeenCalledWith({
        "msg": true
      }, "1/bla");
      return expect(event_receiver.receiver2).toHaveBeenCalledWith({
        "msg": true
      }, "1/bla");
    });
    it('should filter to several receivers', function() {
      mqService.setBaseUrl("sse/");
      mqService.on("1/bla", event_receiver.receiver1);
      mqService.on("*/bla", event_receiver.receiver2);
      mqService.broadcast("2/bla", {
        "msg": true
      });
      expect(event_receiver.receiver2).toHaveBeenCalledWith({
        "msg": true
      }, "2/bla");
      return expect(event_receiver.receiver1).not.toHaveBeenCalled();
    });
    return it('should use the backend to register to messages', function() {
      var called, msg, p1, p2, unregs;
      mqService.setBaseUrl("ws/");
      called = [];
      unregs = [];
      p1 = mqService.on("1/bla", event_receiver.receiver1);
      p2 = mqService.on("*/bla", event_receiver.receiver2);
      p1.then(function(unreg) {
        called.push('p1');
        return unregs.push(unreg);
      });
      p2.then(function(unreg) {
        called.push('p2');
        return unregs.push(unreg);
      });
      ws.readyState = 1;
      ws.onopen();
      expect(ws.send).toHaveBeenCalledWith('{"cmd":"startConsuming","path":"1/bla","_id":2}');
      expect(ws.send).toHaveBeenCalledWith('{"cmd":"startConsuming","path":"*/bla","_id":3}');
      ws.onmessage({
        data: '{"msg":"OK","code":200,"_id":3}'
      });
      ws.onmessage({
        data: '{"msg":"OK","code":200,"_id":2}'
      });
      $rootScope.$apply();
      expect(called).toEqual(["p1", "p2"]);
      msg = '{"m": {"buildid": 1}, "k": "1/bla"}';
      ws.onmessage({
        data: msg
      });
      expect(event_receiver.receiver1).toHaveBeenCalledWith({
        "buildid": 1
      }, "1/bla");
      expect(event_receiver.receiver2).toHaveBeenCalledWith({
        "buildid": 1
      }, "1/bla");
      called = [];
      p1 = unregs[0]();
      p2 = unregs[1]();
      $rootScope.$apply();
      expect(ws.send).toHaveBeenCalledWith('{"cmd":"stopConsuming","path":"1/bla","_id":4}');
      expect(ws.send).toHaveBeenCalledWith('{"cmd":"stopConsuming","path":"*/bla","_id":5}');
      p1.then(function(unreg) {
        return called.push('p1');
      });
      p2.then(function(unreg) {
        return called.push('p2');
      });
      expect(called).toEqual([]);
      ws.onmessage({
        data: '{"msg":"OK","code":200,"_id":4}'
      });
      ws.onmessage({
        data: '{"msg":"OK","code":200,"_id":5}'
      });
      $rootScope.$apply();
      return expect(called).toEqual(["p1", "p2"]);
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('recent storage service', function() {
    var $q, $rootScope, $window, injected, recentStorage;
    recentStorage = $q = $window = $rootScope = null;
    injected = function($injector) {
      $q = $injector.get('$q');
      $window = $injector.get('$window');
      $rootScope = $injector.get('$rootScope');
      return recentStorage = $injector.get('recentStorage');
    };
    beforeEach(inject(injected));
    it('should store recent builds', function(done) {
      var testBuild1, testBuild2, testBuild3;
      testBuild1 = {
        link: '/test1',
        caption: 'test1'
      };
      testBuild2 = {
        link: '/test2',
        caption: 'test2'
      };
      testBuild3 = {
        link: '/test3',
        caption: 'test3'
      };
      recentStorage.clearAll().then(function(e) {
        return $q.all([recentStorage.addBuild(testBuild1), recentStorage.addBuild(testBuild3)]).then(function() {
          return recentStorage.getBuilds().then(function(e) {
            var resolved;
            resolved = e;
            expect(resolved).not.toBeNull();
            expect(resolved).toContain(testBuild1);
            expect(resolved).toContain(testBuild3);
            expect(resolved).not.toContain(testBuild2);
            return done();
          });
        });
      }, function() {
        expect($window.indexedDB).toBeUndefined();
        return done();
      });
      return $rootScope.$digest();
    });
    it('should store recent builders', function(done) {
      var testBuilder1, testBuilder2, testBuilder3;
      testBuilder1 = {
        link: '/test1',
        caption: 'test1'
      };
      testBuilder2 = {
        link: '/test2',
        caption: 'test2'
      };
      testBuilder3 = {
        link: '/test3',
        caption: 'test3'
      };
      recentStorage.clearAll().then(function(e) {
        return $q.all([recentStorage.addBuilder(testBuilder1), recentStorage.addBuilder(testBuilder3)]).then(function() {
          return recentStorage.getBuilders().then(function(e) {
            var resolved;
            resolved = e;
            expect(resolved).not.toBeNull();
            expect(resolved).toContain(testBuilder1);
            expect(resolved).toContain(testBuilder3);
            expect(resolved).not.toContain(testBuilder2);
            return done();
          });
        });
      }, function() {
        expect($window.indexedDB).toBeUndefined();
        return done();
      });
      return $rootScope.$digest();
    });
    return it('should clear all recent builds and builders', function(done) {
      var testBuild1, testBuild2, testBuilder1, testBuilder2;
      testBuild1 = {
        link: '/test1',
        caption: 'test1'
      };
      testBuild2 = {
        link: '/test2',
        caption: 'test2'
      };
      testBuilder1 = {
        link: '/test1',
        caption: 'test1'
      };
      testBuilder2 = {
        link: '/test2',
        caption: 'test2'
      };
      $q.all([recentStorage.addBuild(testBuild1), recentStorage.addBuild(testBuild2), recentStorage.addBuilder(testBuilder1), recentStorage.addBuilder(testBuilder2)]).then(function() {
        return recentStorage.clearAll().then(function(e) {
          return recentStorage.getAll().then(function(e) {
            var resolved;
            resolved = e;
            expect(resolved).toBeDefined();
            expect(resolved.recent_builds.length).toBe(0);
            expect(resolved.recent_builders.length).toBe(0);
            return done();
          });
        });
      }, function() {
        expect($window.indexedDB).toBeUndefined();
        return done();
      });
      return $rootScope.$digest();
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('results service', function() {
    var injected, resultsService;
    resultsService = null;
    injected = function($injector) {
      return resultsService = $injector.get('resultsService');
    };
    beforeEach(inject(injected));
    it('should provide correct results2class', function() {
      var results, results2class;
      results = resultsService.results;
      results2class = function(r) {
        return resultsService.results2class({
          results: r
        });
      };
      expect(results2class(results.SUCCESS)).toBe("results_SUCCESS");
      expect(results2class(results.RETRY)).toBe("results_RETRY");
      expect(results2class(1234)).toBe("results_UNKNOWN");
      expect(resultsService.results2class(void 0)).toBe("results_UNKNOWN");
      expect(resultsService.results2class({
        results: void 0
      })).toBe("results_UNKNOWN");
      expect(resultsService.results2class({
        results: void 0,
        complete: false,
        started_at: void 0
      })).toBe("results_UNKNOWN");
      return expect(resultsService.results2class({
        results: void 0,
        complete: false,
        started_at: 10
      }, "pulse")).toBe("results_PENDING pulse");
    });
    return it('should provide correct results2Text', function() {
      var results, results2text;
      results = resultsService.results;
      results2text = function(r) {
        return resultsService.results2text({
          results: r
        });
      };
      expect(results2text(results.SUCCESS)).toBe("SUCCESS");
      expect(results2text(results.RETRY)).toBe("RETRY");
      expect(results2text(1234)).toBe("...");
      expect(resultsService.results2text(void 0)).toBe("...");
      expect(resultsService.results2text({
        results: void 0
      })).toBe("...");
      expect(resultsService.results2text({
        results: void 0,
        complete: false,
        started_at: void 0
      })).toBe("...");
      return expect(resultsService.results2text({
        results: void 0,
        complete: false,
        started_at: 10
      })).toBe("...");
    });
  });

}).call(this);

(function() {
  describe('settingsService', function() {
    var bbSettingsServiceProviderRef;
    bbSettingsServiceProviderRef = "";
    beforeEach(module('common', function(bbSettingsServiceProvider) {
      bbSettingsServiceProviderRef = bbSettingsServiceProvider;
      localStorage.clear();
      bbSettingsServiceProvider.addSettingsGroup({
        name: 'User',
        caption: 'User related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox1',
            default_value: false
          }, {
            type: 'choices',
            name: 'radio',
            default_value: 'radio1',
            answers: [
              {
                name: 'radio1'
              }, {
                name: 'radio2'
              }
            ]
          }
        ]
      });
      bbSettingsServiceProvider.addSettingsGroup({
        name: 'Release',
        caption: 'Release related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_release',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_release2',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_release3',
            default_value: false
          }, {
            type: 'choices',
            name: name,
            default_value: 'radio1',
            answers: [
              {
                name: 'radio1'
              }, {
                name: 'radio2'
              }
            ]
          }
        ]
      });
      return null;
    }));
    it('should merge groups when old group has values already set', inject(function(bbSettingsService) {
      var group_result, new_group, old_group;
      localStorage.clear();
      old_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            value: true,
            default_value: false
          }
        ]
      };
      new_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            default_value: false
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, new_group);
      return expect(group_result).toEqual({
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            value: true,
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            value: false,
            default_value: false
          }
        ]
      });
    }));
    it('should merge groups when new group is defined with no items', inject(function(bbSettingsService) {
      var group_result, new_group, old_group;
      localStorage.clear();
      old_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            value: true,
            default_value: false
          }
        ]
      };
      new_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: []
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, new_group);
      return expect(group_result).toEqual({
        name: 'Auth',
        caption: 'Auth related settings',
        items: []
      });
    }));
    it('should merge groups when old group is defined with no items', inject(function(bbSettingsService) {
      var group_result, new_group, old_group;
      localStorage.clear();
      old_group = {
        name: 'System',
        caption: 'System related settings',
        items: []
      };
      new_group = {
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2',
            default_value: false
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, new_group);
      return expect(group_result).toEqual({
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2',
            value: false,
            default_value: false
          }
        ]
      });
    }));
    it('should merge groups when new group is undefined', inject(function(bbSettingsService) {
      var group_result, old_group;
      localStorage.clear();
      old_group = {
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2',
            default_value: false
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, void 0);
      return expect(group_result).toBeUndefined();
    }));
    it('should merge groups when old group is undefined', inject(function(bbSettingsService) {
      var group_result, new_group;
      localStorage.clear();
      new_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            default_value: false
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(void 0, new_group);
      return expect(group_result).toEqual({
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            value: false,
            default_value: false
          }
        ]
      });
    }));
    it('should not add a group without name', inject(function(bbSettingsService) {
      var exceptionRun, group;
      localStorage.clear();
      group = {
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            default_value: false
          }
        ]
      };
      exceptionRun = function() {
        var group_result;
        return group_result = bbSettingsServiceProviderRef.addSettingsGroup(group);
      };
      return expect(exceptionRun).toThrow();
    }));
    it('should merge groups when new group has item with no default value', inject(function(bbSettingsService) {
      var group_result, new_group, old_group;
      localStorage.clear();
      old_group = {
        name: 'System',
        caption: 'System related settings',
        items: []
      };
      new_group = {
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2'
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, new_group);
      return expect(group_result).toEqual({
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2',
            value: void 0
          }
        ]
      });
    }));
    it('should generate correct settings', inject(function(bbSettingsService) {
      var groups;
      groups = bbSettingsService.getSettingsGroups();
      return expect(groups['Release']).toEqual({
        name: 'Release',
        caption: 'Release related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_release',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_release2',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_release3',
            value: false,
            default_value: false
          }, {
            type: 'choices',
            name: name,
            default_value: 'radio1',
            value: 'radio1',
            answers: [
              {
                name: 'radio1'
              }, {
                name: 'radio2'
              }
            ]
          }
        ]
      });
    }));
    it('should return correct setting', inject(function(bbSettingsService) {
      var userSetting1, userSetting2, userSetting3;
      userSetting1 = bbSettingsService.getSetting('User.checkbox1');
      userSetting2 = bbSettingsService.getSetting('User.whatever');
      userSetting3 = bbSettingsService.getSetting('UserAA.User_checkbox1');
      expect(userSetting1).toBeDefined();
      expect(userSetting2).toBeUndefined();
      return expect(userSetting3).toBeUndefined();
    }));
    return it('should save correct settings', inject(function(bbSettingsService) {
      var checkbox, storageCheckbox, storageGroups;
      checkbox = bbSettingsService.getSetting('User.checkbox1');
      expect(checkbox.value).toBe(false);
      checkbox.value = true;
      bbSettingsService.save();
      storageGroups = angular.fromJson(localStorage.getItem('settings'));
      storageCheckbox = storageGroups['User'].items[0].value;
      return expect(storageCheckbox).toBeTruthy();
    }));
  });

}).call(this);
