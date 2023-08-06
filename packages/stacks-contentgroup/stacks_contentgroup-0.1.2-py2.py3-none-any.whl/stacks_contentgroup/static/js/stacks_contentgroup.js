
var StacksImage = require('./stacks_image');

var stacksImage = new StacksImage();

var settings = (function() {
    // Any global config should go here
    return {
        animationSpeed: 1000,
        version: "Stacks v0.0.1"
    }
})();

function animatedScroll(el, offset, fn){
    $.when( $('html,body').animate({
        scrollTop: el.offset().top + offset
    }, settings.animationSpeed) ).done(fn());
}


settings.animationSpeed *= .5; // animations for this module UI should be a little faster, dont-cha think????
settings.scrollOffset = 0;
var el = $('.js-stacks-contentgroup'),
    ACTIVE_CONST = "active-contentgroup",
    modules = []; // register modules so we can destroy them later

function Nested(el){
    this.el = $(el);
    this.triggers = this.el.find(".js-stacks-contentgroup-trigger");
    this.rowContainer = this.el.find('.js-contentgroup-content-row');
    this.opened = [];
    this.nestedArticles = this.el.find(".js-contentgroup-content-outer");
    this.initialize(this.triggers); // self-initiating when new Nested() is called
}
Nested.prototype = {
    initialize: function(triggers){
        var self = this;

        this.closeAllOnResize();

        this.trackSubModules();

        triggers.each(function(i) {
            // open article handler
            self.setupArticleOpen($(this), i);
            // close article handler
            self.setupArticleClose($(this), i);
        });
    },
    trackSubModules: function(){
        // keep track of the subModules by using their index position in jQuery collection as an ID number
        this.nestedArticles.find('.js-contentgroup-content-inner').each(function(){
            //$(this).data('opened', false);
        });

    },
    closeAllOnResize: function(){

        var self = this;
        var currentWidth = 'skinny';
        if(matchMedia('only screen and (min-width: 890px)').matches){
            currentWidth = 'wide';
        }

       $(window).resize(function(){
            if(matchMedia('only screen and (min-width: 890px)').matches && currentWidth === "skinny"){
                self.closeAll();
                currentWidth = 'wide';
            } else if (matchMedia('only screen and (max-width: 890px)').matches && currentWidth === "wide") {
                self.closeAll();
                currentWidth = 'skinny';
            }
        });

    },
    setupArticleOpen: function(el, index){
        var self = this;
        el.on('click', function(e) {
            var articleToOpen = self.nestedArticles.eq(index);
            self.openArticle(articleToOpen, index);
            self.toggleActive(this);
            e.preventDefault();
        });

    },
    toggleActive: function(activeItem){
        this.clearActiveArticle();
        $(activeItem).parent().addClass(ACTIVE_CONST);
    },
    clearActiveArticle: function(article){
        article ? article.parent().removeClass(ACTIVE_CONST) : this.el.parent().find('.' + ACTIVE_CONST).removeClass(ACTIVE_CONST);
    },
    setupArticleClose: function(el, index){
        var self = this,
            articleToClose = self.nestedArticles.eq(index);

        articleToClose.find('.close').on('click', function(e) {
            self.closeArticle($(this).parent(), el);
            e.preventDefault;
        });
    },
    openArticle: function(el, index){
        var self = this;
        // first close opened one, without animation
        this.closeAll();
        $('img.lazy').trigger('appear');
        // if desktop breakpoint matches ...
        if(matchMedia('only screen and (min-width: 890px)').matches){

            // Clone nested article
            var clonedEl = el.clone(true, true);
                clonedElArticle = clonedEl.find('.js-contentgroup-content-inner');

            // append article and it's wrapping container to .js-contentgroup-content-row
            var rowContainer = el.parents('.media-row').next(); // first get nearest next row container
            rowContainer.append(clonedEl);
            clonedEl.css('display', 'block'); // set display to block it can be scrolled to

            self.scroll(clonedEl, -Math.abs(clonedEl.height() / 2), function(){
                setTimeout(function() {
                    $.when( clonedElArticle.slideDown(settings.animationSpeed) ).done(function(){
                        self.initSubModules(clonedElArticle, index);
                    });
                }, 300);
            });
        } else {
            // if narrow screen/viewport
            var elArticle = el.find('.js-contentgroup-content-inner');

            el.css( {
                'display': 'block'
            });

            self.scroll(el, 0, function(){
                setTimeout(function() {
                    $.when( elArticle.show(0) ).done(function(){
                        self.initSubModules(elArticle, index);
                    });
                }, 300);
            });
        }

    },
    closeArticle: function(el, originalTrigger){
        var self = this;
        // close article, scroll back to position
        $.when( el.slideUp(settings.animationSpeed) ).done(function(){
            self.scroll(originalTrigger, 0/*-Math.abs(el.height() / 2)*/, function(){
                self.clearActiveArticle(originalTrigger);
            });
        });
    },
    closeAll: function(fn){
        this.nestedArticles.hide();
        this.clearActiveArticle();

        // if an article was cloned into the row container, delete it and it's close btn handler
        this.rowContainer.find('.close').off();
        this.rowContainer.empty();

        if(fn) fn();
    },
    scroll: function(el, offset, fn){
        // Scroll is factored out into it's own function in case we want to swap in a different animation scroll behavior
        animatedScroll(el, offset, fn);
    },
    initSubModules: function($parentArticle, index){
        var alreadyOpen = false;
        for (var i = this.opened.length - 1; i >= 0; i--) {
            if(index === this.opened[i]){
                alreadyOpen = true;
                break;
            }
        };

        if(!alreadyOpen){
            stacksImage.lazyLoadImages($parentArticle); // parent needs display: block before we can lazy load imgs
            this.opened.push(index);
        }

        var subCarousel = $parentArticle.find('.carousel');
        //carousel.owlCarousel();
        if(subCarousel.length) carousel.initCarousel(subCarousel, 0, {pagination: true});

    },
    unbindAll: function(){
        this.triggers.off();
        this.nestedArticles.find('.close').off();
        this.rowContainer.empty(); // if an article was cloned into the row container, delete it.;

    }
}

module.exports = {
    init: function(){
        el.each(function(i){
            var module = new Nested( this );
            modules.push(module);
        });
    },

    destroy: function(){
        for (var i = modules.length - 1; i >= 0; i--) {
            modules[i].unbindAll();
        };
    },
    reset: function(fn){
         for (var i = modules.length - 1; i >= 0; i--) {
            modules[i].closeAll(fn);
        };
    }
};
