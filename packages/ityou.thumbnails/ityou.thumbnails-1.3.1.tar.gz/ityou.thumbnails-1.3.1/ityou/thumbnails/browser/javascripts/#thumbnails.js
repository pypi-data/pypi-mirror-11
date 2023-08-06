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


ThumbnailView.prototype.init = function() {
    this.EventHandler();
    
    setTimeout($.proxy(function() {
        // set last activated view
        if(window.ITYOU.storage.get('thumbnail-view') !== null && window.ITYOU.storage.get('thumbnail-view') !== undefined) {
            this.setOption('currentView', window.ITYOU.storage.get('thumbnail-view'));
        }
        
        this.ListingSize(this.getOption('currentView'));
		
		// insert image src path
		$('.document-download, .folder-item.Folder a').each($.proxy(function(k, el) {
		    this.getThumbnail($(el));
		}, this));
    	
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
    
    $('#' + view).addClass('state-active');
    
    // TODO: deprecated window.ITYOU.storage
    window.ITYOU.storage.set('thumbnail-view', view);

    switch(view) {
        case 'thumbail-list-view':
            this.initListView(els);
            break;
        case 'thumbnail-1-column-view':
            this.destroyListView(els);
        
            els.each($.proxy(function(k, el) {
                $(el).removeClass(this.removeColumn(el)).addClass('col-xs-12');
            }, this));
            break;
        case 'thumbnail-2-columns-view':
            this.destroyListView(els);
            
            els.each($.proxy(function(k, el) {
                $(el).removeClass(this.removeColumn(el)).addClass('col-xs-6');
            }, this));
            break;
        case 'thumbnail-3-columns-view':
            this.destroyListView(els);
        
            els.each($.proxy(function(k, el) {
                $(el).removeClass(this.removeColumn(el)).addClass('col-xs-4');
            }, this));
            break;
        case 'thumbnail-standard-view':
            this.destroyListView(els);
        
            els.each($.proxy(function(k, el) {
                $(el).removeClass(this.removeColumn(el)).addClass('col-xs-6 col-md-4 col-lg-3');
            }, this));
            break;
    }
};


ThumbnailView.prototype.initListView = function(els) {
    els.each($.proxy(function(k, el) {
        $(el).removeClass(this.removeColumn(el)).addClass('col-xs-12 list-group');
        
        $(el).find('.thumbnail').addClass('clearfix');
        $(el).find('.thumbnail > a').first().addClass('col-xs-6 col-sm-4 col-md-2');
        $(el).find('.thumbnail > .caption').addClass('col-xs-6 col-sm-8 col-md-10');
    }, this));
};


ThumbnailView.prototype.destroyListView = function(els) {
    els.each($.proxy(function(k, el) {
        var $thumbnail = $(el).find('.thumbnail'),
            $a = $thumbnail.find('> a').first(),
            $caption = $thumbnail.find('.caption');
    
        $(el).removeClass('col-xs-12 list-group');
        $thumbnail.removeClass('clearfix');
        $a.removeClass(this.removeColumn($a[0]));
        
        if($caption.length > 0) {
            $caption.removeClass(this.removeColumn($caption[0]));
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
    $('#thumbnail-view').on('click', '.thumbnail-listing-size', $.proxy(function(e) {
        e.preventDefault();
    
        var $target = $(e.target),
            size = (e.target.nodeName.toLowerCase() === 'a' ? $target.attr('id') : $target.parents('a').attr('id')),
            $eventTrigger = $('#' + size);
            
        if(!$eventTrigger.hasClass('state-active')) {
            $(e.currentTarget).find('a').each($.proxy(function(k, el) {
                $(el).removeClass('state-active');
            }, this));
            
            return this.ListingSize(size);
        }
        
        return false;
    }, this));
    
    
    $('#thumbnail-view div.folder-item:not(.list-group) div.thumbnail').hoverIntent($.proxy(this.hoverIntentOver, this), $.proxy(this.hoverIntentOut, this));
    
    
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
    
    
    $('#thumbnail-view').on('click', '.thumbnail-listing-sort a', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.target),
            action = $el.data('sortby'),
            direction = $el.data('sort-direction') || 'asc',
            $parent = $el.parents('.thumbnail-listing-sort');
            
        $parent.find('a').each($.proxy(function(k, el) {
            if($el.attr('id') !== $(el).attr('id')) {
                $(el).removeClass('sort-asc sort-desc');
            }
        }, this));
            
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
                
                this.sortDirection($el, direction);

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
                
                this.sortDirection($el, direction);
                
                titles = this.sortAlphabetic(titles, direction);
                
                var items = this.prepareSortedItems(titles);
                
                this.tableSort($('#thumbnail-view').find('form'), items);
            
                break;
        }
    }, this));
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


ThumbnailView.prototype.hoverIntentOver = function(event) {
    var $el = $(event.currentTarget),
        $addInfo = $el.find('div.additional-information'),
        h = $addInfo.css('height', 'auto').height(),
        $toolbar = $el.find('.toolbar'),
        toolbarHeight = $toolbar.find('input[type="checkbox"]').is(':checked') ? false : $toolbar.css('height', 'auto').height();
        
    if(toolbarHeight !== false) {
        $toolbar.show().css('height', 0).animate({
            height: toolbarHeight
        }, 200);
    }
    
    $addInfo.show().css('height', 0).animate({
        height: h,
        padding: '5px'
    }, 400);
};


ThumbnailView.prototype.hoverIntentOut = function(event) {
    var $el = $(event.currentTarget);
    
    $el.find('div.additional-information').animate({
        height: 0,
        padding: 0
    }, 100, function() {
        $(this).hide();
    });
    
    var $toolbar = $el.find('.toolbar');
    
    if(!$toolbar.find('input[type="checkbox"]').is(':checked')) {
        $toolbar.animate({
            height: 0
        }, 100, function() {
            $(this).hide();
        });
    }
};


ThumbnailView.prototype.getMoreThumbs = function() {
    this.showSpinner();
    
    var hiddenItems = $('#thumbnail-view').find('.folder-item:hidden');
    
    if(this.getOption('currentView') === 'thumbnail-standard-view') {
        hiddenItems.slice(0, (Math.ceil($('#portal-column-content').width() / ($('.folder-item').width() + 14)) * 2)).fadeIn(600);
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
};


ThumbnailView.prototype.showSpinner = function() {
    var $spinner = $('<div id="mr-spinner" style="text-align: center; position: absolute; left: 0; right: 0; bottom: 50px;"/>');
    
    $spinner.html('<i class="fa fa-spinner fa-spin" style="font-size: 72px;"/>');
    $spinner.appendTo('#thumbnail-view');
};


ThumbnailView.prototype.hideSpinner = function() {
    $('#mr-spinner').remove();
};


ThumbnailView.prototype.getThumbnail = function(item) {
    $.getJSON(item.attr('href') + '/@@ajax-get-thumbnail', $.proxy(function(response) {
        if(response) {
            item.parents('.folder-item').find('img.img-responsive').attr('src', response);
        }
    }, this));
};


ThumbnailView.prototype.prepContentView = function() {
    var $contentViews = $('.show-preview #content-views').children();

    $contentViews.on('click', function(e) {
        var url = $(this).find('a').attr('href');
        
        if(undefined !== url) {
            window.location = url;
        }
    });
    
    $contentViews.each(function() {
        var menu_context = $(this).find('a').html();
        
        $(this).prepend('<div class="content-view-box"/>');
        $(this).find('.content-view-box').html(menu_context).hide();
        $(this).find('a').html('');
    });
    
    $contentViews.hover(function() {
        if($(this).find('.content-view-box').html().length > 1) {
            $(this).find('.content-view-box').show();
        }
    }, function() {
        $(this).find('.content-view-box').hide();
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



/*
function prepContentViews(){
	        $(".show-preview #content-views").children().click( function() {
	        	var url = $(this).find("a").attr("href");
	        	if (url != undefined) {
	        		window.location = url;
	        	};
	        });
	        $(".show-preview #content-views").children().each(function(){
	        	
	        	var menu_context = $(this).find("a").html();
	        	
	        	$(this).prepend('<div class="content-view-box"></div>');
	        	$(this).find(".content-view-box").html(menu_context).hide();
	        	$(this).find("a").html("");
	        	
	        });
	        
	        $(".show-preview  #content-views").children().hover( function() {
	        	if ( $(this).find(".content-view-box").html().length > 1 ) {         		
	        		$(this).find(".content-view-box").show();
	        	};
	        }, function(){
	        	$(this).find(".content-view-box").hide();
	        });
		}        

*/
$(function() {
        var thumbnails = new ThumbnailView();
        thumbnails.init();



/*    	
    	width = $("#portal-column-content").width();
    	items_to_show = parseInt(width / ($(".folder-item").width() + 14)) * 2;    	
    	$(".folder-item").slice(0, items_to_show - 1).show();
    	if($(".folder-item:visible").length == $(".folder-item").length)
    	{
    		$(".more-item").hide();
    	}

		function getThumbnail(item) {
			$.getJSON(item.attr("href") + "/@@ajax-get-thumbnail", function(data){
				if(data){
					//item_image = item.parent().find(".thumbnail");
					item_image = item.parents('.folder-item').find('img.img-responsive');
					item_image.attr("src", data);
				}
			});			
		}

		$(".document-download").each(function(){
			getThumbnail($(this));
		})

		$(".folder-item.Folder a").each(function(){
			getThumbnail($(this));
		})

		function get_more_thumbnails() {
			$("#spinner").show();
    		$(".folder-item:hidden").slice(0,parseInt($("#portal-column-content").width() / ($(".folder-item").width() + 14)) - 1).fadeIn(600);
    		if($(".folder-item:hidden").length > 0){
		    	$(".folder-item:visible").last().one('inview', function(event, visible){
		    		if(visible){
		    			$("#spinner").show();
		    			get_more_thumbnails();
		    		}
				});
    		}
			$("#spinner").hide();
			if( $('#thumbnail-view form').children().length > 1  ) {
	        	if($(".folder-item:visible").length == $(".folder-item").length) {
	        		$(".more-item").hide();
	        	}
        	}
		}*/
   	
    	/*$(".folder-item:visible").last().one('inview', function(event, visible){
    		if(visible){
    			$("#spinner").show();
    			
    			get_more_thumbnails();
    		}
    	});*/
    	
    	/*$(".more-item").click(function(event){
    		event.preventDefault();
    		get_more_thumbnails();
    	})*/
    	
    	/*$('#thumbnail-view').on('click', '.more-item', function(e) {
    	    e.preventDefault();
    	    
    	    get_more_thumbnails();
    	});*/

        // --------------------------- contentViews ------        
/*
        function prepContentViews(){
	        $(".show-preview #content-views").children().click( function() {
	        	var url = $(this).find("a").attr("href");
	        	if (url != undefined) {
	        		window.location = url;
	        	};
	        });
	        $(".show-preview #content-views").children().each(function(){
	        	
	        	var menu_context = $(this).find("a").html();
	        	
	        	$(this).prepend('<div class="content-view-box"></div>');
	        	$(this).find(".content-view-box").html(menu_context).hide();
	        	$(this).find("a").html("");
	        	
	        });
	        
	        $(".show-preview  #content-views").children().hover( function() {
	        	if ( $(this).find(".content-view-box").html().length > 1 ) {         		
	        		$(this).find(".content-view-box").show();
	        	};
	        }, function(){
	        	$(this).find(".content-view-box").hide();
	        });
		}       
        // --------------------------- /contentViews ------

	$('.linked-document').prepOverlay({
	    subtype: 'ajax',
	    width: "533px",
	    height: "50px",
	    config: {
	    	onLoad: function(e){prepContentViews()}	
	    }
	    
	});
	$('.Image').find(".linked-document").prepOverlay({
	    subtype: 'ajax',
	    width: "800px",
	    height: "50px",
	    config: {
	    	onLoad: function(e){prepContentViews()}	
	    }
	});
	
	
	*/
	
	

	
	//$('#thumbnail-view div.folder-item div.thumbnail').hoverIntent(thumbnailHoverIntent_over, thumbnailHoverIntent_out);
	
	
	/*function thumbnailHoverIntent_over() {
        var el = $(this).find('div.additional-information'),
            h = el.css('height', 'auto').height(),
            toolbar = $(this).find('.toolbar'),
            toolbarHeight = toolbar.find('input[type="checkbox"]').is(':checked') ? false : toolbar.css('height', 'auto').height();
            
        if(toolbarHeight !== false) {
            toolbar.show().css('height',0).animate({
                height: toolbarHeight
            }, 200);
        }
        
        
        el.show().css({
            height: 0
        }).animate({
            height: h,
            padding: '5px'
        }, 400);
	}
	
	function thumbnailHoverIntent_out(obj) {
	    $(this).find('div.additional-information').animate({
            height: 0,
            padding: 0
        }, 100, function() {
            $(this).hide();
        });
        
        var $toolbar = $(this).find('.toolbar');
        
        if(!$toolbar.find('input[type="checkbox"]').is(':checked')) {
            $toolbar.animate({
                height: 0
            }, 100, function() {
                $(this).hide();
            });
        }
	}
	

	$(document).delegate('#thumbnail-view input[type="checkbox"]', 'click', function() {
        var el = $(this).parents('.folder-item');
        if($(this).is(':checked')) {
            el.addClass('state-checked');
        } else {
            el.removeClass('state-checked');
        }
	});
	
	
	
	
	setTimeout(function() {
	    resizeThumbnailView(window.ITYOU.storage.get('thumbnail-view'));
    }, 1);
	
	
	$(document).on('click', '#thumbnail-view .thumbnail-listing-size', function(e) {
	    var $target = $(e.target),
	        $targetLink = $target.parent(),
	        attrId = $target.parent().attr('id');
	        
        $target.parents('.thumbnail-listing-size').find('a').each(function() {
            $(this).removeClass('state-active');
        });
	    
	    resizeThumbnailView(attrId);
	    
	    $targetLink.addClass('state-active');
	    window.ITYOU.storage.set('thumbnail-view', attrId);
	});
	
	
	function resizeThumbnailView(view) {
	    var elements = $('#thumbnail-view').find('.folder-item, .more-item');
	
	    switch(view) {
	        case 'thumbnail-list-view':
	            // TODO
	            break;
	            
            case 'thumbnail-1-column-view':
                elements.each(function() {
                    $(this).removeClass(toRemove(this)).addClass('col-xs-12');
                });
                break;
	            
            case 'thumbnail-2-columns-view':
                elements.each(function() {
                    $(this).removeClass(toRemove(this)).addClass('col-xs-6');
                });
                break;
                
            case 'thumbnail-3-columns-view':
                elements.each(function() {
                    $(this).removeClass(toRemove(this)).addClass('col-xs-4');
                });
                break;
                
            case 'thumbnail-standard-view':
                elements.each(function() {
                    $(this).removeClass(toRemove(this)).addClass('col-xs-6 col-md-4 col-lg-3');
                });
                break;
	    }
	}
	
	
	function toRemove(self) {
	    toReturn = '';
        classes = self.className.split(' ');
        for(i in classes) {
            if(/col-/i.exec(classes[i])) {
                toReturn += classes[i] + ' ';
            }
        }
        return toReturn;
	}*/
	
	
});
