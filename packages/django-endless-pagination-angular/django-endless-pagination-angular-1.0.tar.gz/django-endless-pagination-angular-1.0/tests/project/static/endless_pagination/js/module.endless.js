'use strict';
var App = angular.module('EndlessPagination', []);

App.directive('endlessPagination', function($http) {
    return function (scope, element, attrs) {

        var defaults = {
            // Twitter-style pagination container selector.
            containerSelector: '.endless_container',
            // Twitter-style pagination loading selector.
            loadingSelector: '.endless_loading',
            // Twitter-style pagination link selector.
            moreSelector: 'a.endless_more',
            // Digg-style pagination page template selector.
            pageSelector: '.endless_page_template',
            // Digg-style pagination link selector.
            pagesSelector: 'a.endless_page_link',
            // Callback called when the user clicks to get another page.
            onClick: function() {},
            // Callback called when the new page is correctly displayed.
            onCompleted: function() {},
            // Set this to true to use the paginate-on-scroll feature.
            paginateOnScroll: false,
            // If paginate-on-scroll is on, this margin will be used.
            paginateOnScrollMargin : 1,
            // If paginate-on-scroll is on, it is possible to define chunks.
            paginateOnScrollChunkSize: 0
        },

        settings = angular.extend(defaults, (attrs.endlessPagination ? eval('(' + attrs.endlessPagination + ')') : ""));

        var getContext = function(link) {
            return {
                key: link.attr('rel').split(' ')[0],
                url: link.attr('href')
            };
        };

        return angular.forEach(element, function() {
            var loadedPages = 1;

            // Twitter-style pagination.
            element.on('click', settings.moreSelector, function() {
                var link = angular.element(this),
                html_link = link.get(0),
                container = link.closest(settings.containerSelector),
                loading = container.find(settings.loadingSelector);
                // Avoid multiple Ajax calls.
                if (loading.is(':visible')) {
                    return false;
                }
                link.hide();
                loading.show();
                var context = getContext(link);
                //For get function onClick
                if(typeof settings.onClick == 'string'){
                    var onClick = scope.$eval(settings.onClick);
                }else{
                    var onClick = settings.onClick;
                }
                //For get function onComplete
                if(typeof settings.onCompleted == 'string'){
                    var onCompleted = scope.$eval(settings.onCompleted);
                }else{
                    var onCompleted = settings.onCompleted;
                }
                // Fire onClick callback.
                if (onClick.apply(html_link, [context]) !== false) {
                    // Send the Ajax request.
                    $http({
                        method: "GET",
                        url: context.url,
                        params: {querystring_key: context.key},
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    }).success(function(fragment){
                        container.before(fragment);
                        container.remove();
                        // Increase the number of loaded pages.
                        loadedPages += 1;
                        // Fire onCompleted callback.
                        onCompleted.apply(html_link, [context, fragment.trim()]);
                    });
                }
                return false;
            });

            // On scroll pagination.
            if (settings.paginateOnScroll) {
                var win = angular.element(window),
                doc = angular.element(document);
                win.scroll(function(){
                    if (doc.height() - win.height() -
                        win.scrollTop() <= settings.paginateOnScrollMargin) {
                        // Do not paginate on scroll if chunks are used and
                        // the current chunk is complete.
                        var chunckSize = settings.paginateOnScrollChunkSize;
                        if (!chunckSize || loadedPages % chunckSize) {
                            element.find(settings.moreSelector).click();
                        }
                    }
                });
            }

            // Digg-style pagination.
            element.on('click', settings.pagesSelector, function() {
                var link = angular.element(this),
                html_link = link.get(0),
                context = getContext(link);
                //For get function onClick
                if(typeof settings.onClick == 'string'){
                    var onClick = scope.$eval(settings.onClick);
                }else{
                    var onClick = settings.onClick;
                }
                //For get function onComplete
                if(typeof settings.onCompleted == 'string'){
                    var onCompleted = scope.$eval(settings.onCompleted);
                }else{
                    var onCompleted = settings.onCompleted;
                }
                // Fire onClick callback.
                if (onClick.apply(html_link, [context]) !== false) {
                    var page_template = link.closest(settings.pageSelector);
                    $http({
                        method: "GET",
                        url: context.url,
                        params: {querystring_key: context.key},
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    }).success(function(fragment){
                        angular.element(page_template).html(fragment);
                        onCompleted.apply(html_link, [context, fragment.trim()]);
                    });
                }
                return false;
            });
        });
    };
});