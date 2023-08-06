/*
 * composer.js
 */
(function($, root) {
  "use strict";

  var edit_modal_html = '<div class="reveal-modal" data-reveal>' + 
      '<h3>Edit the <span class="element-name"></span> element</h3><hr>' +
      '<div class="modal-content"></div>' +
      '<div class="modal-submit radius button">Save</div>' +
      '<a class="close-reveal-modal">&times;</a>' +
    '</div>';


  var Editor = function(el) {
    this.el = el;
    this.name = el.data('name');
    this.url = el.data('url');

    this.modal = $(edit_modal_html);
    $('body').append(this.modal);
    $(root.document).foundation('reveal', 'reflow');

    this.init();
  };

  Editor.prototype = {
    init: function() {
      var view = this;

      this.el.find('.edit-composer-button').on('click', function() {
        view.show();
      });

      this.modal.find('.modal-submit').on('click', function() {
        view.submit();
      });

      this.modal.find('form').on('submit', function(event) {
        event.preventDefault();
        view.submit();
      });

      this.modal.find('.element-name').text(this.name);
    },

    show: function() {
      this.modal.foundation('reveal', 'open');
      this.fetch();
    },

    hide: function() {
      this.modal.foundation('reveal', 'close');
    },

    busy: function() {
      this.modal.find('.modal-content').html('<img src="/static/img/loader.gif"><p>Loading...</p>');
    },

    fetch: function() {
      var content = this.modal.find('.modal-content'),
          request = $.get(this.url);

      this.busy();

      request.success(function(data) {
        content.html(data);
      });
      request.fail(function() {
        content.html('<p>Could not load the element, try refreshing the page and try again.</p>');
      });
    },

    serialize_form: function() {
      var form = this.modal.find('form'),
          data = {};

      $.each(form.serializeArray(), function() { data[this.name] = this.value; });
      return data;
    },

    submit: function() {
      var content = this.modal.find('.modal-content'),
          request = $.post(this.url, this.serialize_form());

      this.busy();

      request.success(function(data) {
        root.location.reload();
      });
      request.fail(function(xhr) {
        content.html(xhr.responseText);
      });
    }
  };

  $.fn.composer = function() {
    this.each(function() {
      this._composer_editor = new Editor($(this));
    });
  };

  $(function() {
    $('.edit-composer-element').composer();
  });

})(jQuery, window);