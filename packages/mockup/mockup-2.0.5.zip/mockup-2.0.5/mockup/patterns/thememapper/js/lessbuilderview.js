define([
  'jquery',
  'underscore',
  'backbone',
  'mockup-patterns-filemanager-url/js/basepopover',
  'mockup-patterns-resourceregistry-url/js/iframe'
], function($, _, Backbone, PopoverView, IFrame ) {
  'use strict';
  var lessBuilderTemplate = _.template(
    '<div id="lessBuilder">' +
      '<span class="message"></span>' +
      '<span style="display: none;" class="errorMessage"></span>' +
      '<div class="buttonBox">' +
        '<a id="compileBtn" class="btn btn-success" href="#">Compile</a>' +
        '<a id="errorBtn" class="btn btn-default" href="#">Clear</a>' +
      '</div>' +
    '</div>'
  );

  var LessBuilderView = PopoverView.extend({
    className: 'popover lessbuilderview',
    title: _.template('<%= _t("LESS Builder") %>'),
    content: lessBuilderTemplate,
    $button: null,
    $start: null,
    $working: null,
    $done: null,
    $error: null,
    render: function() {
      var self = this;
      PopoverView.prototype.render.call(this);
      self.$message = $('.message', this.$el);
      self.$error = $('.errorMessage', this.$el);
      self.$button = $('#compileBtn', this.$el);
      self.$errorButton = $('#errorBtn', this.$el);
      self.$button.on('click', function() {
        self.showLessBuilder();
      });
      self.$errorButton.on('click', function() {
        self.start();
        self.toggle();
      });
      self.start();
      return this;
    },
    toggle: function(button, e) {
      PopoverView.prototype.toggle.apply(this, [button, e]);
    },
    start: function() {
      var self = this;
      self.$button.show();
      self.$errorButton.hide();
      self.$message.text("Click to compile the current file");
      self.$error.hide();
    },
    working: function() {
      var self = this;
      self.$button.hide();
      self.$message.text("Working....");
    },
    end: function() {
      var self = this;
      self.$message.text("Compiled successfully");
      setTimeout(self.reset.bind(self), 3000);
    },
    reset: function() {
      var self = this;
      self.start();
      self.toggle();
    },
    showError: function(error) {
      this.$message.text("");
      this.$error.text(error).show();
      this.$errorButton.show();
    },
    showLessBuilder: function() {
      var self = this;

      if( self.app.lessPaths['save'] === undefined ) {
        self.showError("Error: invalid filetype");
        return false;
      }

      self.working();

      var config = {
        less: [ self.app.lessVariableUrl,
                self.app.lessPaths['less'],
                self.app.lessUrl]
      }

      var iframe = new IFrame({
        name: 'lessc',
        resources: config.less,
        callback: self.app.saveThemeCSS,
        env: self.app,
        configure: function(iframe){
          iframe.window.lessErrorReporting = function(what, error, href){
            if( error.href !== undefined )
            {
              self.app.fileManager.ace.editor.scrollToLine(error.line, true);
              if( error.type == "Name" ) {
                var reg = new RegExp(".*(@\\S+)\\s.*");
                var matches = reg.exec(error.message);
                if( matches !== null ) {
                  var varName = matches[1];
                  var result = self.app.fileManager.ace.editor.findAll(varName);
                }
              }
              else {
                //The line number is always off by 1? (and LESS indexes from 0) so -2
                self.app.fileManager.ace.editor.moveCursorToPosition({row: error.line - 2, column: error.column});
                self.app.fileManager.ace.editor.focus();
              }
              self.showError(error);
            }
          };
          iframe.styles = [];
        },
        onLoad: function(self) {
          less.pageLoadFinished.then(
            function() {
              var $ = window.parent.$;
              var iframe = window.iframe['lessc'];
              var styles = $('style', iframe.document);
              var styleBox = $('#styleBox');

              $(styleBox).empty();
              $(styles).each(function() {
                styleBox.append(this.innerHTML);
              });

              iframe.options.callback();
            }
          );
        }
      });

    },
  });

  return LessBuilderView;
});
