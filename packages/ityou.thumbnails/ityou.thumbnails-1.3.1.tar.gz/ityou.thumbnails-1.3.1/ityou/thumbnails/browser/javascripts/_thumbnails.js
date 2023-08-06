/*(function($) {
    $.fn.equalHeights = function(minHeight, maxHeight) {
        this.find('.thumbnail').each(function() {
            $(this).height('auto');
        });
    
        tallest = (minHeight) ? minHeight : 0;
        
        //console.log('min: ' + minHeight, 'max: ' + maxHeight, 'tallest: ' + tallest);
        
        setTimeout($.proxy(function() {
            this.each(function() {
                if($(this).height() > tallest) {
                    tallest = $(this).height();
                }
            });
            
            if((maxHeight) && tallest > maxHeight) {
                tallest = maxHeight;
            }
            
            if(tallest % 10 !== 0) {
                 var r = tallest % 10;
                 
                 tallest += (10 - r);
            }
            
            return this.each(function() {
                $(this).find('.thumbnail').animate({'height': tallest}, 100).css('overflow', 'hidden');
            });
        }, this), 100);
    }
})(jQuery);





function ThumbnailView(options) {
	this.options = $.extend({}, {
        currentView: 'thumbnail-standard-view'
    }, options);
    
    this.getOptions = function() {
        return this.options;
    };
    
    this.getOption = function(option) {
        if(this.options.hasOwnProperty(option)) {
            return this.options[option];
        }
        
        return false;
    };
    
    this.setOption = function(option, value) {
        this.options[option] = value;
    };
};

//ThumbnailView.prototype = new Utilities();


ThumbnailView.prototype.init = function() {
    this.EventHandler();
    
    setTimeout($.proxy(function() {
        // set last activated view
    	//this.storage.local.set('activitiesTimestamp', $(activityList).find('li.activity').first().data('timestamp'));
    	//console.log(this.storage.local.get('thumbnail-view'));
        if(window.ITYOU.storage.get('thumbnail-view') !== null && window.ITYOU.storage.get('thumbnail-view') !== undefined) {
            this.setOption('currentView', window.ITYOU.storage.get('thumbnail-view'));
        }
        
        this.ListingSize(this.getOption('currentView'));
		
        // insert image src path
        this.getThumbnail($('.document-download, .folder-item.Folder a'), 0);
		//$('.document-download, .folder-item.Folder a').each($.proxy(function(k, el) {
			//this.getThumbnail($(el), k == l, [k, l]);
		//}, this));
    	
    	// show some items
    	$('#thumbnail-view').find('.folder-item').slice(0, (Math.ceil($('#portal-column-content').width() / ($('.folder-item').width() + 14)) * 2)).show();
    	
    	// hide 'more item' element if all items are visible
    	if($('#thumbnail-view').find('.folder-item:visible').length === $('#thumbnail-view').find('.folder-item').length && $('#thumbnail-view').find('.folder-item').length > 0) {
    	    $('.more-item').hide();
    	}
    	
    	
    	// transform timestamps
    	//this.addUnixTimestamp();
    }, this), 1);
};


ThumbnailView.prototype.ListingSize = function(view) {
    var els = $('#thumbnail-view').find('.folder-item, .more-item');
    
    if(!$('#' + view).hasClass('state-active') && !$('#' + view).prop('disabled')) {
    	$('#' + view)
    		.addClass('state-active')
    		.prop('disabled', true);
    }
    
    // TODO: deprecated window.ITYOU.storage
    window.ITYOU.storage.set('thumbnail-view', view);

    switch(view) {
        case 'thumbail-list-view':
            this.initListView(els);
            break;
        case 'thumbnail-1-column-view':
            this.initGridView(els, 'col-xs-12');
            break;
        case 'thumbnail-2-columns-view':
            this.initGridView(els, 'col-xs-6');
            break;
        case 'thumbnail-3-columns-view':
            this.initGridView(els, 'col-xs-4');
            break;
        case 'thumbnail-standard-view':
            this.initGridView(els, 'col-xs-6 col-md-4 col-lg-3');
            break;
    }
    
    els.equalHeights();
};


ThumbnailView.prototype.initGridView = function(items, column) {
    this.destroyListView(items);

    items.each($.proxy(function(k, el) {
        $(el).removeClass(this.removeColumn(el)).addClass(column);
    }, this));
};


ThumbnailView.prototype.initListView = function(els) {
    els.each($.proxy(function(k, el) {
        $(el).removeClass(this.removeColumn(el)).addClass('col-xs-12 list-group');
        
        $(el).find('.thumbnail').addClass('clearfix');
        $(el).find('.thumbnail > a').first().addClass('col-xs-6 col-sm-4 col-md-2');
        $(el).find('.thumbnail > .caption').addClass('col-xs-6 col-sm-8 col-md-10');
        $(el).find('.thumbnail > .additional-information').addClass('col-xs-6 col-sm-8 col-md-10');
    }, this));
};

ThumbnailView.prototype.destroyListView = function(els) {
    els.each($.proxy(function(k, el) {
        var $thumbnail = $(el).find('.thumbnail'),
            $a = $thumbnail.find('> a').first(),
            $caption = $thumbnail.find('.caption'),
            $addInfo = $thumbnail.find('.additional-information');
    
        $(el).removeClass('col-xs-12 list-group');
        $thumbnail.removeClass('clearfix');
        $a.removeClass(this.removeColumn($a[0]));
        
        if($caption.length > 0) {
            $caption.removeClass(this.removeColumn($caption[0]));
        }
        
        if($addInfo.length > 0) {
            $addInfo.removeClass(this.removeColumn($addInfo[0]));
        }
    }, this));
};


ThumbnailView.prototype.removeColumn = function(el) {
    var tmp = new Array(),
        classNames = el.className.split(' ');
    
    for(i in classNames) {
        if(/col-/i.exec(classNames[i])) {
            tmp.push(classNames[i]);
        }
    }
    
    return tmp.join(' ');
};


ThumbnailView.prototype.EventHandler = function() {
    $(window).on('resize', $.proxy(function(e) {
        $('#thumbnail-view .folder-item, #thumbnail-view .more-item').equalHeights();
    }, this));


    $('#thumbnail-view .thumbnail-listing-size').on('click', 'button', $.proxy(function(e) {
    //$('#thumbnail-view').on('click', '.thumbnail-listing-size', $.proxy(function(e) {
        e.preventDefault();
        
        // close all opened additional informations
        this.hideAdditionalInformations();
        
        var $target = $(e.target),
            //size = (e.target.nodeName.toLowerCase() === 'a' ? $target.attr('id') : $target.parents('a').attr('id')),
        	size = (e.target.nodeName.toLowerCase() === 'button' ? $target.attr('id') : $target.parents('button').attr('id')),
            $eventTrigger = $('#' + size);
        
        if(!$eventTrigger.hasClass('state-active')) {
            //$(e.currentTarget).find('a').each($.proxy(function(k, el) {
        	$('#thumbnail-view .thumbnail-listing-size').find('button').each($.proxy(function(k, el) {
                $(el).removeClass('state-active');
        		if($(el).prop('disabled')) {
        			$(el).removeProp('disabled');
        		}
            }, this));
            
            return this.ListingSize(size);
        }
        
        return false;
    }, this));
    
    
    $('#thumbnail-view').on('change', 'input[type="checkbox"]', $.proxy(function(e) {
        var $target = $(e.currentTarget),
            $el = $target.parents('.folder-item');
            
        if($target.prop('checked') === true) {
            $el.addClass('state-checked');
        } else {
            $el.removeClass('state-checked');
        }
	}, this));
	
	
	$('#thumbnail-view').find(".folder-item:visible").last().one('inview', $.proxy(function(event, visible) {
		if(visible) {
		    this.getMoreThumbs();
		}
	}, this));
	
	
	$('#thumbnail-view').on('click', '.more-item', $.proxy(function(e) {
	    e.preventDefault();
	    
	    this.getMoreThumbs();
	}, this));
	
	    
    $('.linked-document').prepOverlay({
        subtype: 'ajax',
        width: '533px',
        height: '50px',
        config: {
            onLoad: $.proxy(function(e) {
                this.prepContentView();
            }, this)
        }
    });
    
    $('.Image').find('.linked-document').prepOverlay({
        subtype: 'ajax',
	    width: "800px",
	    height: "50px",
	    config: {
	    	onLoad: $.proxy(function(e) {
	    	    this.prepContentView();
	    	}, this)
	    }
    });
    
    
    
    $('#thumbnail-view').on('click', '.thumbnail-listing-sort a, #thumbnail-listing-sort-method', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.target),
            action = $el.data('sortby'), // creation_date/modification_date/thumb_list_title
            direction = $('#thumbnail-listing-sort-method').data('sort-direction') || 'asc';
        
        if(!$el.hasClass('btn')) {
        	var btn = $('#thumbnail-listing-sort-method');
        	var btnText = $el.text();
        	
        	btn
        		.text(btnText)
        		.data('sortby', action);
        }
        
        /*$parent.find('a').each($.proxy(function(k, el) {
            if($el.attr('id') !== $(el).attr('id')) {
                $(el).removeClass('sort-asc sort-desc');
            }
        }, this));*/
/*            
        $('#thumbnail-view').find('.folder-item').show();
        
        switch(action) {
            case 'creation_date':
            case 'modification_date':
                var timestamps = [];
                
                var sortingRule = action === 'creation_date' ? 'date_created' : 'date_edited';

                $('#thumbnail-view').find('.additional-information').find('span.' + sortingRule).each($.proxy(function(k, el) {
                    var key = $(el).parents('.folder-item').attr('id');
                
                    timestamps.push([key, $.trim($(el).data('unix'))]);
                }, this));
                
                this.sortDirection($('#thumbnail-listing-sort-method'), direction);

                timestamps = this.sortNumeric(timestamps, direction);
                
                var items = this.prepareSortedItems(timestamps);
                
                this.tableSort($('#thumbnail-view').find('form'), items);
                
                break;
            
            case 'title':
                var titles = [];
                
                $('#thumbnail-view').find('.thumbnail .caption').each($.proxy(function(k, el) {
                    var key = $(el).parents('.folder-item').attr('id');
                    
                    titles.push([key, $.trim($(el).text())]);
                }, this));
                
                this.sortDirection($('#thumbnail-listing-sort-method'), direction);
                
                titles = this.sortAlphabetic(titles, direction);
                
                var items = this.prepareSortedItems(titles);
                
                this.tableSort($('#thumbnail-view').find('form'), items);
            
                break;
        }
    }, this));
    
    
    
    $('#thumbnail-view div.folder-item:not(.list-group) div.thumbnail').hoverIntent($.proxy(this.hoverIntentOverToolbar, this), $.proxy(this.hoverIntentOutToolbar, this));
    
    
    $('#thumbnail-view div.folder-item:not(.list-group) div.thumbnail').on('click', '.additional-information-trigger', $.proxy(function(e) {
        e.preventDefault();

        this.toggleAdditionalInformation(e);
    }, this));
    //.hoverIntent($.proxy(this.showAdditionalInformation, this), $.proxy(this.hideAdditionalInformation, this));
    
};


ThumbnailView.prototype.sortDirection = function(el, direction) {
    if(direction === 'asc') {
        el.data('sort-direction', 'desc').removeClass('sort-desc').addClass('sort-asc');
    } else {
        el.data('sort-direction', 'asc').removeClass('sort-asc').addClass('sort-desc');
    }
};

ThumbnailView.prototype.prepareSortedItems = function(data) {
    var items = [];
    
    $.each(data, $.proxy(function(k, v) {
        var $item = $('#thumbnail-view').find('#' + v[0]);
        
        items.push($item);
    }, this));
    
    return items;
};


ThumbnailView.prototype.hideAdditionalInformations = function() {
    $('#thumbnail-view .folder-item').find('.thumbnail').find('.additional-information').find('.holder').each(function() {
        if($(this).is(':visible')) {
            $(this).slideToggle({
                direction: 'down',
                duration: 100
            });
        }
    });
};


ThumbnailView.prototype.toggleAdditionalInformation = function(e) {
    var $wrapper = $(e.currentTarget).parents('.thumbnail'),
        $addInfo = $wrapper.find('.additional-information'),
        $holder = $addInfo.find('.holder');
        
    var wasVisible = $holder.is(':visible');
        
    this.hideAdditionalInformations();
        
    if(!wasVisible) {
        $holder.slideToggle({
            direction: 'up',
            duration: 300
        });
    }
};


// unused
ThumbnailView.prototype.showAdditionalInformation = function(event) {
    var $el = $(event.currentTarget).parents('.thumbnail'),
        $addInfo = $el.find('div.additional-information'),
        $holder = $addInfo.find('.holder');
        
    $holder.slideToggle({
        direction: 'up',
        duration: 300
    });
};


// unused
ThumbnailView.prototype.hideAdditionalInformation = function(event) {
    var $el = $(event.currentTarget).parents('.thumbnail'),
        $addInfo = $el.find('div.additional-information'),
        $holder = $addInfo.find('.holder');

    $holder.slideToggle({
        direction: 'down',
        duration: 300
    });
};


ThumbnailView.prototype.hoverIntentOverToolbar = function(event) {
    var $el = $(event.currentTarget),
        $toolbar = $el.find('.toolbar'),
        $toolbarHolder = $toolbar.find('.holder');
        
    if(!$toolbar.find('input[type="checkbox"]').is(':checked')) {
        $toolbarHolder.fadeIn(100);
    }
};


ThumbnailView.prototype.hoverIntentOutToolbar = function(event) {
    var $el = $(event.currentTarget),
        $toolbar = $el.find('.toolbar'),
        $toolbarHolder = $toolbar.find('.holder');
        
    if(!$toolbar.find('input[type="checkbox"]').is(':checked')) {
        $toolbarHolder.fadeOut(100);
    }
};


ThumbnailView.prototype.getMoreThumbs = function() {
    this.showSpinner();
    
    var hiddenItems = $('#thumbnail-view').find('.folder-item:hidden');
    
    if(this.getOption('currentView') === 'thumbnail-standard-view') {
        hiddenItems.slice(0, (Math.ceil($('#portal-column-content').width() / ($('.folder-item').width() + 14)) * 2)).fadeIn(600);
    } else if(this.getOption('currentView') === 'thumbnail-1-column-view' || this.getOption('currentView') === 'thumbail-list-view') {
    	hiddenItems.slice(0, 2).fadeIn(600);
    } else {
        hiddenItems.slice(0, (Math.ceil($('#portal-column-content').width() / ($('.folder-item').width() + 14)) - 1)).fadeIn(600);
    }
    
    if($('#thumbnail-view').find('.folder-item:hidden').length > 0) {
        $('#thumbnail-view').find('.folder-item:visible').last().one('inview', $.proxy(function(e, visible) {
            if(visible) {
                this.getMoreThumbs();
            }
        }, this));
    }
    
    this.hideSpinner();
    
    if($('#thumbnail-view form').children().length > 1 && $('#thumbnail-view').find('.folder-item:visible').length === $('#thumbnail-view').find('.folder-item').length) {
        $('#thumbnail-view').find('.more-item').hide();
    }
    
    this.ListingSize(this.getOption('currentView'));
    
    //console.log('hiddenItems: ' + hiddenItems.length, 'Math: ' + (Math.ceil($('#portal-column-content').width() / ($('.folder-item').width() + 14)) - 1));
    //console.log('currentView: ' + this.getOption('currentView'));
};


ThumbnailView.prototype.showSpinner = function() {
    var $spinner = $('<div id="mr-spinner" style="text-align: center; position: absolute; left: 0; right: 0; bottom: 50px;"/>');
    
    $spinner.html('<i class="fa fa-spinner fa-spin" style="font-size: 72px;"/>');
    $spinner.appendTo('#thumbnail-view');
};


ThumbnailView.prototype.hideSpinner = function() {
    $('#mr-spinner').remove();
};


ThumbnailView.prototype.getThumbnail = function(items, offset) {
	var item = $(items[offset]);
	var length = items.length;
	
	$.getJSON(item.attr('href') + '/@@ajax-get-thumbnail', $.proxy(function(response) {
        if(response) {
            var path = response.replace(/size=(.*)/g, 'size=large');
        
            item.parents('.folder-item').find('img.img-responsive').attr('src', path);
        }
        
        // resizing here, rest is not visible
        if((offset > 1 && !item.is(':visible') && $(items[offset-1]).is(':visible')) || (offset == length-1 && item.is(':visible'))) {
    		this.ListingSize(this.getOption('currentView'));
    	}
    	
    	if(offset < length-1) {
        	this.getThumbnail(items, ++offset);
        }
    }, this));
};


ThumbnailView.prototype.prepContentView = function() {
    var $contentViews = $('.show-preview #content-views').children(),
        color = 'text-primary';

    $contentViews.on('click', function(e) {
        var url = $(this).find('a').attr('href');
        
        if(undefined !== url) {
            window.location = url;
        }
    });
    
    $contentViews.each(function() {
        var menu_context = $(this).find('a').html();
        
        $(this).prepend('<div class="content-view-box"/>');
        $(this).find('.content-view-box').html(menu_context);
        $(this).find('a').html('');
        
        if(!$(this).hasClass('selected')) {
            $(this).find('.content-view-box').addClass(color);
        }
    });
    
    $contentViews.hover(function() {
        if($(this).find('.content-view-box').html().length > 1) {
            var $contentViewBox = $(this).find('.content-view-box');
            
            $contentViewBox
                .removeClass(color)
                .find('.text').show();
        }
    }, function() {
        var $contentViewBox = $(this).find('.content-view-box');
    
        if(!$(this).hasClass('selected')) {
            $contentViewBox.addClass(color);
        }
    
        $contentViewBox.find('.text').hide();
    });
    
    
};


ThumbnailView.prototype.addUnixTimestamp = function() {
    $('#thumbnail-view').find('.folder-item').find('.additional-information').find('span.date_created').each($.proxy(function(k, el) {
        $(el).data('unix', this.convertToUNIXTimestamp($(el).text()));
    }, this));
};



ThumbnailView.prototype.convertToUNIXTimestamp = function(timestamp) {
    var tmp = timestamp.split('.');
    var tmpDate = new Date();
    tmpDate.setDate(tmp[0]);
    tmpDate.setMonth((tmp[1]-1));
    tmpDate.setFullYear(tmp[2]);

    return Math.floor(Date.parse(tmpDate) / 1000);
};


ThumbnailView.prototype.tableSort = function(table, rows) {
    var $moreItem = $('<div>').append(table.find('.more-item').clone()).html();

    table.empty();
    
    $.each(rows, $.proxy(function(k, row) {
        table.append(row);
    }, this));
    
    table.append($moreItem);
};


ThumbnailView.prototype.sortNumeric = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        a = a[1];
        b = b[1];
    
        return a-b;
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};


ThumbnailView.prototype.sortAlphabetic = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        var a = a[1].toLowerCase(),
            b = b[1].toLowerCase();
        
        return a.localeCompare(b);
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};


ThumbnailView.prototype.getMaxHeight = function(element) {
    return Math.max.apply(null, element.map(function() {
        return $(this).height();
    }).get());
};





$(function() {
    var thumbnails = new ThumbnailView();
    thumbnails.init();
});
*/