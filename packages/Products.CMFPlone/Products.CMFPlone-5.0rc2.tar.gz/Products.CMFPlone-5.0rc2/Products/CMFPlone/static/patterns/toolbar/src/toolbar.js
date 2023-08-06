define([
  'jquery',
  'mockup-patterns-base',
  'pat-registry',
  'mockup-utils',
  'translate',
  'jquery.cookie'
], function ($, Base, Registry, utils, _t) {
  'use strict';

  var Toolbar = Base.extend({
    name: 'toolbar',
    trigger: '.pat-toolbar',
    defaults: {
      containerSelector: '#edit-zone',
      classNames: {
        logo: 'plone-toolbar-logo',
        left: 'plone-toolbar-left',
        leftDefault: 'plone-toolbar-left-default',
        leftExpanded: 'plone-toolbar-left-expanded',
        top: 'plone-toolbar-top',
        topDefault: 'plone-toolbar-top-default',
        topExpanded: 'plone-toolbar-top-expanded',
        expanded: 'plone-toolbar-expanded',
        active: 'active'
      },
      cookieName: 'plone-toolbar'
    },
    setupMobile: function(){
      var that = this;
      that.$container.css('right', '-120px');
      // make sure we are in expanded mode
      $('body').addClass(that.options.classNames.leftExpanded);
      $('body').addClass(that.options.classNames.expanded);
      $('body').addClass(that.options.classNames.left);
      $('body').removeClass(that.options.classNames.topExpanded);
      $('body').removeClass(that.options.classNames.top);
      $('body').removeClass(that.options.classNames.topDefault);
      $('.' + that.options.classNames.logo, that.$container).off('click').on('click', function() {
        var $el = $(this);
        if ($el.hasClass('open')){
          that.$container.css('right', '-120px');
          $('html').css('margin-left', '0');
          $('html').css('margin-right', '0');
          $el.removeClass('open');
          $('nav li', that.$container).removeClass(that.options.classNames.active);
        } else {
          that.$container.css('right', '0');
          $el.addClass('open');
          $('html').css('margin-left', '-120px');
          $( 'html' ).css('margin-right', '120px');
        }
      });
      $('nav li a', that.$container).has('.plone-toolbar-caret').off('click').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var $el = $(this).parent();
        if ($el.hasClass(that.options.classNames.active)) {
          that.$container.css('right', '0');
          $('html').css('margin-left', '-120px');
          $('html').css('margin-right', '120px');
          $('nav li', that.$container).removeClass(that.options.classNames.active);
        } else {
          $('nav li', that.$container).removeClass(that.options.classNames.active);
          $el.addClass(that.options.classNames.active);
          that.$container.css('right', '180px');
          $('html').css('margin-left', '-300px');
          $('html').css('margin-right', '300px');
        }
      });
    },
    setupDesktop: function(){
      var that = this;
      if(that.state.expanded){
        $('body').addClass(that.options.classNames.expanded);
      }else{
        $('body').removeClass(that.options.classNames.expanded);
      }

      $('.' + that.options.classNames.logo, that.$container).off('click').on('click', function() {
        if (that.state.expanded) {
          // currently expanded, need to compress
          that.setState({
            expanded: false
          });
          $('body').removeClass(that.options.classNames.expanded);
          $('nav li', that.$container).removeClass(that.options.classNames.active);
          if (that.state.left) {
            $('body').addClass(that.options.classNames.leftDefault);
            $('body').removeClass(that.options.classNames.leftExpanded);
          } else {
            $('body').addClass(that.options.classNames.topDefault);
            $('body').removeClass(that.options.classNames.topExpanded);
          }
        } else {
          that.setState({
            expanded: true
          });
          // Switch to expanded
          $('body').addClass(that.options.classNames.expanded);
          $('nav li', that.$container).removeClass(that.options.classNames.active);
          if (that.state.left) {
            $('body').addClass(that.options.classNames.leftExpanded);
            $('body').removeClass(that.options.classNames.leftDefault);
          } else {
            $('body').addClass(that.options.classNames.topExpanded);
            $('body').removeClass(that.options.classNames.topDefault);
          }
        }
      });

      $('nav > ul > li li', that.$container).off('click').on('click', function(event) {
        event.stopImmediatePropagation();
      });

      // active
      $('nav > ul > li', that.$container).has( 'a .plone-toolbar-caret' ).off('click').on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        var hasClass = $(this).hasClass(that.options.classNames.active);
        // always close existing
        $('nav li', that.$container).removeClass(that.options.classNames.active);
        $('nav li > ul', $(this)).css({'margin-top': ''}); // unset this so we get fly-in affect
        if (!hasClass) {
          // open current selected if not already open
          $(this).addClass(that.options.classNames.active);
          that.padPulloutContent($(this));
        }
      });

      $('body').on('click', function(event) {
        if (!($(this).parent(that.options.containerSelector).length > 0)) {
          $('nav > ul > li', that.$container).each(function(key, element){
            $(element).removeClass(that.options.classNames.active);
          });
        }
      });
      that.setHeight();
    },
    padPulloutContent: function($li){
      if(!this.state.left || !this.isDesktop()){
        // only when on left
        return;
      }
      // try to place content as close to the user click as possible
      var $content = $('> ul', $li);
      var $inner = $content.find('> *');
      var $first = $inner.first();
      var $last = $inner.last();
      var insideHeight = ($last.position().top - $first.position().top) + $last.outerHeight();
      var height = $content.outerHeight();

      var itemLocation = $li.position().top || $li.offset().top;  // depends on positioning
      // margin-top + insideHeight should equal total height
      $content.css({
        'margin-top': Math.min(itemLocation, height - insideHeight)
      });
    },
    isDesktop: function(){
      return $(window).width() > '768';
    },
    _setHeight: function(){
      var $items = $('.plone-toolbar-main', this.$container);
      $items.css({height: ''});
      var natualHeight = $items.outerHeight();
      $('.scroll-btn', this.$container).remove();

      $items.css({
        'padding-top': ''
      });
      var height = $(window).height() - $('#personal-bar-container').height() -
        $('.plone-toolbar-logo').height();

      if(height < natualHeight){
        /* add scroll buttons */
        var $scrollUp = $('<li class="scroll-btn up"><a href="#"><span class="icon-up"></span><span>&nbsp;</span></a></li>');
        var $scrollDown = $('<li class="scroll-btn down"><a href="#"><span class="icon-down"></span><span>&nbsp;</span></a></li>');
        $items.prepend($scrollUp);
        $items.append($scrollDown);
        height = height - $scrollDown.height();
        $items.height(height);
        $items.css({
          'padding-top': $scrollUp.height()
        });
        $scrollUp.click(function(e){
          e.preventDefault();
          $items.scrollTop($items.scrollTop() - 50);
        });
        $scrollDown.click(function(e){
          e.preventDefault();
          $items.scrollTop($items.scrollTop() + 50);
        });
      }
      /* if there is active, make sure to reposition */
      var $active = $('li.active ul:visible', this.$container);
      if($active.size() > 0){
        this.padPulloutContent($active);
      }
    },
    setHeight: function(){
      if(!this.state.left || !this.isDesktop()){
        // only when on left
        return;
      }
      var that = this;
      clearTimeout(that.heightTimeout);
      that.heightTimeout = setTimeout(function(){
        that._setHeight();
      }, 50);
    },
    setState: function(state){
      var that = this;
      that.state = $.extend({}, that.state, state);
      /* only cookie configurable attribute is expanded or contracted */
      $.cookie(that.options.cookieName, JSON.stringify({
        expanded: that.state.expanded
      }), {path: '/'});
    },
    hideElements: function(){
      if(this.state.left){
        // only when on top
        return;
      }
      var w = $('.plone-toolbar-container').width(),
          wtc = $('.plone-toolbar-logo').width();
      $( ".plone-toolbar-main > li" ).each(function() {
        wtc += $(this).width();
      });

      $('#personal-bar-container > li').each(function() {
        wtc += $(this).width();
      });
      wtc -= $('#plone-toolbar-more-options').width();
      if (w < wtc) {
        if (!($('#plone-toolbar-more-options').length)) {
          $('[id^="plone-contentmenu-"]').hide();
          $('.plone-toolbar-main').append('<li id="plone-toolbar-more-options"><a href="#"><span class="icon-moreOptions" aria-hidden="true"></span><span>' + _t('More') + '</span><span class="plone-toolbar-caret"></span></a></li>');
          $('#personal-bar-container').after('<ul id="plone-toolbar-more-subset" style="display: none"></ul>');
          $( "[id^=plone-contentmenu-]" ).each(function() {
            $(this).clone(true, true).appendTo( "#plone-toolbar-more-subset" );
            $('[id^=plone-contentmenu-]', '#plone-toolbar-more-subset').show();
          });
          $('#plone-toolbar-more-options a').on('click', function(event){
            event.preventDefault();
            $('#plone-toolbar-more-subset').toggle();
          });
        }
      } else {
        $('[id^="plone-contentmenu-"]').show();
        $('#plone-toolbar-more-options').remove();
        $('#plone-toolbar-more-subset').remove();
      }

    },
    init: function () {
      var that = this;
      that.heightTimeout = 0;
      that.$container = $(that.options.containerSelector);
      var toolbar_cookie = $.cookie(that.options.cookieName);
      that.state = {
        expanded: true,
        left: $('body').hasClass(that.options.classNames.left)
      };
      if(toolbar_cookie){
        try{
          that.state = $.extend({}, that.state, $.parseJSON(toolbar_cookie));
        }catch(e){
          // ignore
        }
      }

      if (that.isDesktop()){
        that.setupDesktop();
        if (!that.state.left) {
          // in case its top lets just hide what is not needed
          that.hideElements();
        }
      }else {
        that.setupMobile();
      }
      this.$el.addClass('initialized');

      /* folder contents changes the context.
         This is for usability so the menu changes along with
         the folder contents context */
      $('body').off('structure-url-changed').on('structure-url-changed', function (e, path) {
        $.ajax({
          url: $('body').attr('data-portal-url') + path + '/@@render-toolbar'
        }).done(function(data){
          var $el = $(utils.parseBodyTag(data));
          that.$el.replaceWith($el);
          Registry.scan($el);
        });
      });

      $(window).on('resize', function(){
        if (that.isDesktop()){
          that.setupDesktop();
          if (!that.state.left) {
            // in case its top lets just hide what is not needed
            that.hideElements();
          }
        }else {
          that.setupMobile();
        }
      });
    },

  });

  return Toolbar;
});
