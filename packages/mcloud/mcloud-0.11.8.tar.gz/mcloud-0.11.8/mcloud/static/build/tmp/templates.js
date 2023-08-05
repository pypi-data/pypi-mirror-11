(function(module) {
try { module = angular.module("templates"); }
catch(err) { module = angular.module("templates", []); }
module.run(["$templateCache", function($templateCache) {
  "use strict";
  $templateCache.put("src/common/footer.tpl.html",
    "<div class=\"pure-g\">\n" +
    "  <div class=\"pure-u-1 text-center\">\n" +
    "    <p>&copy; 2014 - <a href=\"http://alessandro.arnodo.net\">Alessandro Arnodo.</a>\n" +
    "  </div>\n" +
    "  <div class=\"pure-u-1 text-center\">\n" +
    "    <ul class=\"hlist\">\n" +
    "      <li><a target=\"_blank\" href=\"http://twitter.com/vesparny\">twitter</a>\n" +
    "      </li>\n" +
    "      <li><a target=\"_blank\" href=\"https://plus.google.com/+AlessandroArnodo\">g+</a>\n" +
    "      </li>\n" +
    "      <li><a target=\"_blank\" href=\"http://www.linkedin.com/in/alessandroarnodo\">LinkedIn</a>\n" +
    "      </li>\n" +
    "      <li><a target=\"_blank\" href=\"https://github.com/vesparny/angular-kickstart\">GitHub</a>\n" +
    "      </li>\n" +
    "    </ul>\n" +
    "  </div>\n" +
    "</div>\n" +
    "");
}]);
})();

(function(module) {
try { module = angular.module("templates"); }
catch(err) { module = angular.module("templates", []); }
module.run(["$templateCache", function($templateCache) {
  "use strict";
  $templateCache.put("src/common/header.tpl.html",
    "<div class=\"pure-menu pure-menu-open pure-menu-horizontal\">\n" +
    "  <a class=\"pure-menu-heading\" href=\"\">angular-kickstart <span app-version></span></a>\n" +
    "  <ul>\n" +
    "    <li ui-sref-active=\"pure-menu-selected\"><a href ui-sref=\"root.home\">{{ 'home' | uppercase }}</a>\n" +
    "    </li>\n" +
    "    <li ui-sref-active=\"pure-menu-selected\"><a href ui-sref=\"root.getting-started\">{{ 'getting started' | uppercase }}</a>\n" +
    "    </li>\n" +
    "  </ul>\n" +
    "</div>\n" +
    "");
}]);
})();

(function(module) {
try { module = angular.module("templates"); }
catch(err) { module = angular.module("templates", []); }
module.run(["$templateCache", function($templateCache) {
  "use strict";
  $templateCache.put("src/app/getting-started/getting-started.tpl.html",
    "<div class=\"pure-g island3\">\n" +
    "  <div class=\"content pure-u-1\">\n" +
    "    <p class=\"island-panel\">\n" +
    "      <strong>Note that this is only a getting started guide, for more detailed information about the build system, the available tasks, the configuration of the build or anything else, please refer to the <a href=\"https://github.com/vesparny/angular-kickstart/#readme\" target=\"_blank\">documentation</a> on the GitHub project.</strong>\n" +
    "    </p>\n" +
    "\n" +
    "    <h3>What and Why</h3>\n" +
    "    <p>\n" +
    "      <code>angular-kickstart</code> is an opinionated kickstart for single page application development with AngularJS. It makes your development and testing easy, keeps the structure of the project consistent and allows you to create a fully optimized\n" +
    "      production release withe ease. After having developed a lot of AngularJS projects I decided to collect here what I've learnt.\n" +
    "    </p>\n" +
    "\n" +
    "    <h3>Getting started</h3>\n" +
    "    <p>\n" +
    "      Install\n" +
    "      <strong><a href=\"https://github.com/joyent/node/wiki/installation\" target=\"_blank\">node.js</a></strong>. Then\n" +
    "      <strong>sass, gulp and bower</strong> if you haven't yet.\n" +
    "    </p>\n" +
    "\n" +
    "    <pre>\n" +
    "    <code>\n" +
    "    $ gem install sass\n" +
    "    $ npm -g install gulp bower\n" +
    "    </code>\n" +
    "</pre>\n" +
    "\n" +
    "    <p>\n" +
    "      After that, install\n" +
    "      <code>angular-kickstart</code> - download the <a href=\"https://github.com/vesparny/angular-kickstart/releases/latest\">latest</a> release (or clone the master branch if want to run the development version). Unzip the project and cd into it, then\n" +
    "      install bower and npm dependencies, and run the application in development mode.\n" +
    "    </p>\n" +
    "\n" +
    "    <pre>\n" +
    "    <code>\n" +
    "    $ npm install\n" +
    "    $ bower install\n" +
    "    $ gulp serve\n" +
    "    </code>\n" +
    "</pre>\n" +
    "\n" +
    "    <p>\n" +
    "      You are now ready to go, your applcation is available at <code>http://127.0.0.1:3000</code>.\n" +
    "    </p>\n" +
    "    <p>\n" +
    "      You are now ready to start coding, every file you add, edit or delete into the\n" +
    "      <code>/client</code> folder, will be handled by the build system and the browser will reload.\n" +
    "    </p>\n" +
    "    <p>\n" +
    "      When you are ready to build a production release there is a task for that.\n" +
    "    </p>\n" +
    "\n" +
    "    <pre>\n" +
    "    <code>\n" +
    "    $ gulp serve:dist\n" +
    "    </code>\n" +
    "</pre>\n" +
    "\n" +
    "    <p>\n" +
    "      This task will lint your code, optimize css js and images files, run unit tests. After the task has successfully finished, you can find an optimized version of your project in the\n" +
    "      <code>/build/dist</code> folder.\n" +
    "    </p>\n" +
    "\n" +
    "    <p>\n" +
    "      Other tasks are available:\n" +
    "    </p>\n" +
    "\n" +
    "    <pre>\n" +
    "    <code>\n" +
    "    #for developing running unit test on every file change.\n" +
    "    $ gulp serve:tdd\n" +
    "\n" +
    "    #for running e2e test. (you application should be running on http://127.0.0.1:3000)\n" +
    "    $ gulp test:e2e\n" +
    "\n" +
    "    #for running unit tests one time then exit.\n" +
    "    $ gulp test:unit\n" +
    "    </code>\n" +
    "</pre>\n" +
    "    <p class=\"text-center\">\n" +
    "      <a href=\"https://github.com/vesparny/angular-kickstart/#readme\" target=\"_blank\" class=\"pure-button button-xlarge pure-button-primary\">\n" +
    "        Full documentation on GitHub\n" +
    "      </a>\n" +
    "    </p>\n" +
    "\n" +
    "  </div>\n" +
    "</div>\n" +
    "</div>\n" +
    "");
}]);
})();

(function(module) {
try { module = angular.module("templates"); }
catch(err) { module = angular.module("templates", []); }
module.run(["$templateCache", function($templateCache) {
  "use strict";
  $templateCache.put("src/app/home/home.tpl.html",
    "");
}]);
})();
