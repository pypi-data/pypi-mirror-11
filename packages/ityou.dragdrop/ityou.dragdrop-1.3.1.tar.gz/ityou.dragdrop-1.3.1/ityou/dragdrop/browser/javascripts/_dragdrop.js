/*function DragDrop() {
	this.draggableOptions = {
        helper: $.proxy(function(event) {
            var el = $(event.currentTarget),
                currentView;
            
            //console.log(event);
            
            var $currentView = $('#thumbnail-view').find('.thumbnail-listing-size').find('a.state-active');
            
            if($currentView.length === 0) {
                currentView = 'col-xs-6 col-md-4 col-lg-3';
            } else {
                if($currentView.attr('id') === 'thumbail-list-view') {
                    currentView = 'list-group';
                } else if($currentView.attr('id') === 'thumbnail-1-column-view') {
                    currentView = 'col-xs-12';
                } else if($currentView.attr('id') === 'thumbnail-2-columns-view') {
                    currentView = 'col-xs-6';
                } else if($currentView.attr('id') === 'thumbnail-3-columns-view') {
                    currentView = 'col-xs-4';
                } else {
                    currentView = 'col-xs-6 col-md-4 col-lg-3';
                }
            }
            
                //console.log('draggable', dnd.getMaxHeight($('#thumbnail-view').find('.folder-item')));
                
            var data = {
                uid: el.attr('id'),
                portal_type: el.attr('data-portal-type'),
                ahref: el.attr('data-url'),
                imgsrc: el.find('img:not(.loading)').attr('src'),
                icon: el.attr('data-contenticon'),
                title: el.find('.item-title').text(),
                elHeight: this.getMaxHeight($('#thumbnail-view').find('.folder-item'))-20,
                //elHeight: parseInt($('#thumbnail-view').find('div.folder-item').first().find('.thumbnail').css('height')) + 10,
                elWidth: parseInt($('#thumbnail-view').find('div.folder-item').first().css('width')),
                currentView: currentView
            };
                
            if(data.portal_type == 'Folder') {
                return $($('#dragdrop-draggableFolder-tmpl').render(data));
            } else {
                return $($('#dragdrop-draggableFile-tmpl').render(data));
            }
        }, this),
        containtment: 'body',
        appendTo: 'body',
        cursor: 'move',
        connectToSortable: '#thumbnail-view form[name="folderContentsForm"]',
        start: function(event, ui) {
            $('#thumbnail-view').find('.folder-item:hidden').fadeIn(600);
        },
        cancel: '.copy-move-item, .delete-item',
    };
	this.draggingTolerance = 10;
    this.floatFix = 2;
    this.sortableSelector = $('#thumbnail-view form[name="folderContentsForm"]');
    this.dragDropContainer = 'dl.portlet-static-drag-drop dd.portletItem p#dragdrop-container div.drag-drop-container';
    

    this.getTwbsCol = function(self) {
	    toReturn = '';
	    classes = self.className.split(' ');
	    for(i in classes) {
	        if(/col-/i.exec(classes[i])) {
	            toReturn += classes[i] + ' ';
	        }
	    }
	    
	    return toReturn;
    };
	
    
	this.checkPermission = function() {
		var permission = false,
			copyPermission = false,
			movePermission = false;
		
		var running1 = true;
		$.getJSON('@@ajax-dragdrop-permissions', {action: 'can_copy'}, $.proxy(function(response) {
			running1 = false;
			
			copyPermission = copyPermission || response;
			permission = permission || response;
		}, this));
		
		var running2 = true;
		$.getJSON('@@ajax-dragdrop-permissions', {action: 'can_move'}, $.proxy(function(response) {
			running2 = false;
			
			movePermission = movePermission || response;
			permission = permission || response;
		}, this));
		
		var timing = setInterval($.proxy(function() {
			if(!running1 && !running2) {
				clearInterval(timing);
				
				console.log("general: " + permission, ", copy: " + copyPermission, ", move: " + movePermission);
				
				if(!permission) {
					$('dl.portlet-static-drag-drop').remove();
				} else {
					this.initDragDrop(copyPermission, movePermission);
				}
			}
		}, this), 50);
	};
	
	
	this.initDragDrop = function(canCopy, canMove) {
		if($('dl.portlet-static-drag-drop').length > 0) {
			$('dl.portlet-static-drag-drop').find('div.copy-move-container').find('.action-bar').each($.proxy(function(k, el) {
				if($(el).hasClass('copy') && !canCopy) {
					$(el).prop('disabled', true);
				} else if($(el).hasClass('move') && !canMove) {
					$(el).prop('disabled', true);
					
					$(el).removeClass('state-active').prev().addClass('state-active');
				}
			}, this));
			
	        $.getJSON('@@ajax-dragdrop', {action: 'get_dragdrop_objects'}, $.proxy(function(response) {
	            if(response.length > 0) {
	                $('dl.portlet-static-drag-drop').find('#dragdrop-portlet-text').hide();
	            
	                $.each(response, function(i, val) {
                        val.thumbnail_class = (val.portal_type == 'Folder' ? '' : 'linked-document link-overlay');
	                        
                        $($('#dragdrop-dragdropcontainer-tmpl').render(val)).appendTo('dl.portlet-static-drag-drop p#dragdrop-container');
	                });
	                
	                $('div.drag-drop-container').each($.proxy(function(k, el) {
	                	var ddEl = $(el),
	                        state = $('dl.portlet-static-drag-drop').find('div.copy-move-container').find('.action-bar.move').hasClass('state-active') ? 'can_move' : 'can_copy';
	                	
	                	this.checkState(ddEl, state);
                    }, this));
                }
	        }, this));
        }
	};
	
	
	this.initDropable = function() {
		$('dl.portlet-static-drag-drop #dragdrop-container').droppable({
            //greedy: true,
            accept: '#thumbnail-view div.folder-item',
            activeClass: 'state-active',
            hoverClass: 'state-hover',
            tolerance: 'pointer',
            drop: $.proxy(function(event, ui) {
                this.droppableDrop(ui.draggable, $('dl.portlet-static-drag-drop #dragdrop-container'));
            }, this)
        });
	};
	
	
	this.initSortable = function() {
		this.sortableSelector.sortable({
            appendTo: 'body',
            cursor: 'move',
            helper: 'clone',
            items: '.folder-item',
            placeholder: 'sorting placeholder',
            containment: 'parent',
            start: $.proxy(function(event, ui) {
                $('#thumbnail-view').find('.folder-item:hidden').fadeIn(600);
                ui.item.hide();
                
                var tmpEl = $('#thumbnail-view').find('.folder-item').first();
                
                if(tmpEl.attr('id') === ui.item.attr('id')) {
                    tmpEl = $('#thumbnail-view').find('.folder-item:eq(1)');
                    
                    if(tmpEl.length === 0) {
                        tmpEl = $('#thumbnail-view').find('.more-item');
                    }
                }
                
                var tmpCol = this.getColumns(tmpEl[0]);
                    
                if(tmpEl.hasClass('list-group')) {
                    tmpCol += ' list-group';
                }
                
                $('#thumbnail-view .sorting.placeholder').addClass(tmpCol).html('<div class="thumbnail"/>');
                
                if($(ui.item).hasClass('drag-drop-container')) {
                    var h = this.getMaxHeight($('#thumbnail-view').find('.folder-item, .more-item'));
                
                    $('#thumbnail-view .sorting.placeholder .thumbnail').height((h - 20));
                    ui.helper.height((h - 20));
                } else {
                    $('#thumbnail-view .sorting.placeholder .thumbnail').height((ui.item.height() - 20));
                    ui.helper.height((ui.item.height() - 20));
                }
                
                setTimeout(function() {
                    $('.folder-item.ui-sortable-helper').find('.additional-information').hide();
                }, 1);
                
                this.sortableSelector.sortable('option', 'cursor', 'move');
            }, this),
            stop: $.proxy(function(event, ui) {
                var distanceTop = (ui.position.top-ui.originalPosition.top) < 0 ? (ui.position.top-ui.originalPosition.top)*(-1) : (ui.position.top-ui.originalPosition.top),
                    distanceLeft = (ui.position.left-ui.originalPosition.left) < 0 ? (ui.position.left-ui.originalPosition.left)*(-1) : (ui.position.left-ui.originalPosition.left);
                
                if(ui.position == undefined || (distanceTop < this.draggingTolerance && distanceLeft < this.draggingTolerance)) {
                    var isFolder = $.inArray('Folder', event.originalEvent.target.classList) > -1 ? true : false;
                    
                    if(event.originalEvent.target.nodeName == 'IMG') {
                        if(isFolder) {
                            location.href = ui.item.find('a').attr('href');
                        } else {
                            ui.item.find('a.link-overlay').trigger('click');
                        }
                    } else {
                        if(ui.item.find('a.document-download').length > 0) {
                            location.href = ui.item.find('a.document-download').attr('href');
                        } else {
                            location.href = ui.item.find('a').attr('href');
                        }
                    }
                }
            }, this),
            update: $.proxy(function(event, ui) {
                var uids = [],
                    selector = this.sortableSelector;
            
                if(ui.item.hasClass('drag-drop-container')) {
                    var uid = ui.item.attr('data-uid');
                    
                    var h = this.getMaxHeight($('#thumbnail-view').find('.folder-item, .more-item'))-20;
                        
                    var data = {
                        id: ui.item.attr('data-id'),
                        uid: uid,
                        portal_type: ui.item.attr('data-portal-type'),
                        contenttype: ('contenttype-'+ui.item.attr('data-portal-type').toLowerCase()),
                        contenticon: ui.item.attr('data-contenticon'),
                        url: ui.item.attr('data-url'),
                        imgsrc: ui.item.find('img:not(.loading)').attr('src'),
                        title: ui.item.find('.item-title').text(),
                        author: ui.item.attr('data-addinfo-author'),
                        created: ui.item.attr('data-addinfo-date-created'),
                        edited: ui.item.attr('data-addinfo-date-edited'),
                        description: ui.item.attr('data-addinfo-description'),
                        aclass: ui.item.attr('data-portal-type') == 'Folder' ? '' : 'linked-document link-overlay',
                        relpb: ($('#thumbnail-view').find('div.folder-item').length+100),
                        elHeight: h
                    };
                    
                    var state = $('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar.copy').hasClass('state-active') ? 'copy_object' : 'move_object';

                    $('#dragdrop-container').find('div[data-uid="'+data.uid+'"]').find('.copy-move-item').hide();
                    $('#dragdrop-container').find('div[data-uid="'+data.uid+'"]').find('.delete-item').hide();
                    $('#dragdrop-container').find('div[data-uid="'+data.uid+'"]').find('.loader').show();
                    
                    var $next = $(ui.item).next('.folder-item'),
                        $prev = $(ui.item).prev('.folder-item'),
                        $more = $('#thumbnail-view').find('.more-item');
                        
                    var tmpEl = $next.length > 0 ? $next : ($prev.length > 0 ? $prev : $more),
                        tmpCol = this.getColumns(tmpEl[0]);
                    
                    ui.item.empty().removeClass().addClass('folder-item').addClass(tmpCol);
                    var placeholderLoading = $('#dragdrop-droppablePlaceholder-tmpl').render();
                    $(placeholderLoading)
                        .height(h)
                        .appendTo(ui.item);
                
                    $.getJSON('@@ajax-dragdrop', {action: state, uid: uid}, $.proxy(function(response) {
                        var uids = [];
                        if(this.castBool(response) == true) {
                            if(state == 'move_object') {
                                $('#thumbnail-view').find('.folder-item#'+uid).remove();
                            }
                            
                            ui.item
                                .empty()
                                .removeClass()
                                .addClass('folder-item '+data.portal_type+' '+data.id)
                                .attr('id', uid)
                                .removeData()
                                .removeAttr('data-portal-type')
                                .removeAttr('data-url')
                                .removeAttr('data-id')
                                .removeAttr('data-uid')
                                .removeAttr('data-addinfo-author')
                                .removeAttr('data-addinfo-created')
                                .removeAttr('data-addinfo-edited')
                                .removeAttr('data-addinfo-description')
                                .removeAttr('data-thumbnail-class')
                                .removeAttr('data-contenticon')
                                .css('display', 'block');
                                
                            var $next = $(ui.item).next('.folder-item'),
                                $prev = $(ui.item).prev('.folder-item'),
                                $more = $('#thumbnail-view').find('.more-item');
                                
                            var tmpEl = $next.length > 0 ? $next : ($prev.length > 0 ? $prev : $more),
                                tmpCol = this.getColumns(tmpEl[0]);
                                
                            ui.item.addClass(tmpCol);
                        
                            if(data.portal_type == 'Folder') {
                                $($('#dragdrop-droppableFolder-tmpl').render(data)).appendTo(ui.item);
                            } else {
                                $($('#dragdrop-droppableItem-tmpl').render(data)).appendTo(ui.item);
                            }
       
                            
                            $('p#dragdrop-container').find('#'+uid).find('span.delete-item').trigger('click');
                            ui.item.attr('id', response);

                            selector.sortable('refresh');
                            selector.sortable('option', 'containment', 'parent');
                            
                            $('.folder-item').each(function() {
                                uids.push($(this).attr('id'));
                            });
                            $.getJSON('@@ajax-sorting', {'order': uids.join()});
                            
                            thumbnailViewPrepOverlay(ui.item, data.portal_type);
                            thumbnailViewHoverIntent();
                        } else {
                            ui.item.fadeOut(200, function() {
                                ui.item.remove();
                            });
                        }
                    }, this));
                } else {
                    var dragdrop = $('dl.portlet-static-drag-drop'),
                        portletWrapperLeft = $('#portal-column-one').find('.portletWrapper').length > 0 ? true : false,
                        portletWrapperRight = $('#portal-column-two').find('.portletWrapper').length > 0 ? true : false,
                        portletLeft = $('#portal-column-one').find('.portletWrapper').first(),
                        portletRight = $('#portal-column-two').find('.portletWrapper').first(),
                        footer = $('#portal-footer');
                        
                    if((portletWrapperRight && (ui.position.left+ui.item.width()) > portletRight.offset().left) || (portletWrapperLeft && (ui.position.left-ui.item.width()) < portletLeft.offset().left) || (ui.position.top+ui.item.height()) < this.sortableSelector.offset().top || (footer.length > 0 && (ui.position.top) > footer.offset().top)) {
                        this.sortableSelector.sortable('cancel');
                    } else {
                    	$('.folder-item').each(function() {
                    		uids.push($(this).attr('id'));
                    	});
                    	$.getJSON('@@ajax-sorting', {'order': uids.join()});
                	}
            	}
            }, this)
        });
	};
	
	
	this.initTrash = function() {
		$.getJSON('@@ajax-dragdrop-permissions', {action:'can_delete'}, $.proxy(function(response) {
           if(this.castBool(response) == true) {
                $('#delete-container').droppable({
                    //greedy: true,
                    accept: '#thumbnail-view div.folder-item',
                    hoverClass: 'state-hover',
                    tolerance: 'pointer',
                    drop: function(event, ui) {
                        var uid = ui.draggable.attr('id'),
                            uids = [];
                        
                        ui.draggable.remove().html('').remove();
                        
                        $.getJSON('@@ajax-dragdrop', {action:'move_to_trash', uid:uid}, $.proxy(function(response) {
                            if(this.castBool(response) == true) {
                                setTimeout(function() {
                                    $('.folder-item#'+uid).html('');
                                    $('#'+uid+'.folder-item').remove();
                                    
                                    $('.folder-item').each(function() {
                                        uids.push($(this).attr('id'));
                                    });
                                    $.getJSON('@@ajax-sorting', {'order': uids.join()});
                                }, 1);
                            }
                        }, this));
                    }
                });
            } else {
                $('#delete-container i').css({color: '#000', opacity: '0.2'});
            }
        }, this));
	};
	
	
	$('#thumbnail-view, dl.portlet-static-drag-drop').disableSelection();
	
	
	this.mouseEventHandler();
	this.keyboardEventHandler();
};


DragDrop.prototype.getColumns = function(el) {
    var tmp = new Array(),
        classNames = el.className.split(' ');
    
    for(i in classNames) {
        if(/col-/i.exec(classNames[i])) {
            tmp.push(classNames[i]);
        }
    }
    
    return tmp.join(' ');
};


DragDrop.prototype.getMaxHeight = function(element) {
    return Math.max.apply(null, element.map(function() {
        return $(this).height();
    }).get());
};


DragDrop.prototype.checkState = function(obj, state) {
	$.getJSON('@@ajax-dragdrop-permissions', {action: state, uid: obj.attr('id')}, $.proxy(function(response) {
		var actionBar = obj.find('.action-bar');
		
        if(this.castBool(response) == true) {
        	obj.draggable(this.draggableOptions);
            obj.removeClass('can-not-move-or-copy');
            
            actionBar.find('.copy-move-item').addClass('fa-arrow-left').removeClass('fa-times').prop('disabled', false);
            actionBar.find('input[type="checkbox"]').prop('disabled', false);
        } else {
        	if(obj.data('uiDraggable')) {
        		obj.draggable('destroy');
        	}
        	
        	actionBar.find('.copy-move-item').removeClass('fa-arrow-left').addClass('fa-times').prop('disabled', true);
        	actionBar.find('input[type="checkbox"]').prop('disabled', true);
        	
            obj.addClass('can-not-move-or-copy');
        }
    }, this));
};


DragDrop.prototype.castBool = function(val) {
    if(typeof val == 'string' && val.toLowerCase() == 'true' || typeof val == 'boolean' && val == true) {
        return true;
    } else if(typeof val == 'string' && val.toLowerCase() == 'false' || typeof val == 'boolean' && val == false) {
        return false;
    } else {
        return true;
    }
};


DragDrop.prototype.moveToTrash = function(obj, uid) {
    var uids = [];
    
    $.getJSON('@@ajax-dragdrop', {action:'move_to_trash', uid:uid}, $.proxy(function(response) {
        if(this.castBool(response) == true) {
            obj.effect('fade', 200, function() {
                setTimeout(function() {
                    obj.remove();
            
                    $('.folder-item').each(function() {
                        uids.push($(this).attr('id'));
                    });
                    
                    $.getJSON('@@ajax-sorting', {'order': uids.join()});
                }, 1);
            });
        }
    }, this));
};



// Copy & Paste from thumbnails.js
DragDrop.prototype.prepContentView = function() {
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

// Copy & Paste from thumbnails.js
DragDrop.prototype.hideAdditionalInformations = function() {
    $('#thumbnail-view .folder-item').find('.thumbnail').find('.additional-information').find('.holder').each(function() {
        if($(this).is(':visible')) {
            $(this).slideToggle({
                direction: 'down',
                duration: 100
            });
        }
    });
};

// Copy & Paste from thumbnails.js
DragDrop.prototype.toggleAdditionalInformation = function(e) {
    this.hideAdditionalInformations();
    
    var $wrapper = $(e.currentTarget).parents('.thumbnail'),
        $addInfo = $wrapper.find('.additional-information'),
        $holder = $addInfo.find('.holder');
        
    if($holder.is(':visible')) {
        $holder.slideToggle({
            direction: 'down',
            duration: 300
        });
    } else {
        $holder.slideToggle({
            direction: 'up',
            duration: 300
        });
    }
};



DragDrop.prototype.droppableDrop = function(ui, obj) {
    var uid = ui.attr('id'),
    	uids = [];

	$('body').find('dd.portletItem p#dragdrop-container').find('div.drag-drop-container').each(function() {
	    uids.push($(this).attr('id'));
	});
	
	if($.inArray(uid, uids) == -1 || uids.length == 0) {
	    $.getJSON('@@ajax-dragdrop', {action: 'add_dragdrop_object', uid: uid}, $.proxy(function(response) {
	        if(this.castBool(response) == true) {
	            $('dl.portlet-static-drag-drop').find('#dragdrop-portlet-text').hide();
	            
	            var data = {
	                uid: uid,
	                portal_type: ui.attr('class').replace(/folder-item /, '').split(' ')[0],
	                id: ui.attr('class').replace(/folder-item /,'').split(' ')[1],
	                url: ui.find('a').attr('href'),
	                icon: ui.find('.item-title').find('img').attr('src'),
	                author: ui.find('.additional-information').find('.author').text(),
	                created: ui.find('.additional-information').find('.date_created').text(),
	                edited: ui.find('.additional-information').find('.date_edited').text(),
	                description: ui.find('.additional-information').find('.item-description').text(),
	                thumbnail_url: ui.find('img.img-responsive').attr('src'),
	                thumbnail_class: ui.find('img').attr('class'),
	                title: ui.find('div.item-title').first().text()
	            };
	
	            //$('#dragdrop-dragdropcontainer-tmpl').tmpl(data).appendTo('dl.portlet-static-drag-drop p#dragdrop-container');
	            $($('#dragdrop-dragdropcontainer-tmpl').render(data)).appendTo('dl.portlet-static-drag-drop p#dragdrop-container');
	            
	            $('dl.portlet-static-drag-drop').find('dd.portletItem p#dragdrop-container').find('div.drag-drop-container#'+uid).each($.proxy(function(k, el) {
	                if(!$(el).hasClass('ui-draggable')) {
	                    var ddEl = $(el);
	                    
	                    if($('div.copy-move-container').find('.state-active').hasClass('copy')) {
	                        $.getJSON('@@ajax-dragdrop', {action: 'can_copy'}, $.proxy(function(response) {
	                            if(this.castBool(response) == true) {
	                                ddEl.draggable(this.draggableOptions);
	                            } else {
	                                ddEl.addClass('can-not-move-or-copy');
	                            }
	                        }, this));
	                    } else {
	                        $.getJSON('@@ajax-dragdrop', {action: 'can_move', uid: uid}, $.proxy(function(response) {
	                            if(this.castBool(response) == true) {
	                                ddEl.draggable(this.draggableOptions);
	                            } else {
	                                ddEl.addClass('can-not-move-or-copy');
	                            }
	                        }, this));
	                    }
	                }
	            }, this));
	        } else {
	            if($('dl.portlet-static-drag-drop').find('dd.portletItem p#dragdrop-container').find('div.drag-drop-container').length == 0) {
	                $('dl.portlet-static-drag-drop').find('dd.portletItem #dragdrop-portlet-text').show();
	            }
	        }
	    }, this));
	}
};


DragDrop.prototype.removeFromDragDrop = function(obj) {
    $.getJSON('@@ajax-dragdrop', {action: 'remove_dragdrop_object', uid: obj.attr('id')});
        
    obj.effect('fade', 500, function() {
        obj.remove();
        
        if($('dl.portlet-static-drag-drop').find('dd.portletItem p#dragdrop-container').find('div.drag-drop-container').length == 0) {
            $('dl.portlet-static-drag-drop').find('#dragdrop-portlet-text').show();
        }
    });
};


DragDrop.prototype.insertToThumbnailView = function(obj, obj_state) {
	var uid = obj.attr('data-uid'),
        state = obj_state == undefined ? ($('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container div.action-bar.copy').hasClass('state-active') ? 'copy_object' : 'move_object') : obj_state + '_object';

    obj.find('.action-bar').find('.copy-move-item').hide();
    obj.find('.action-bar').find('.delete-item').hide();
    obj.find('.action-bar').find('.loader').show();
    
    $.getJSON('@@ajax-dragdrop', {action: state, uid: uid}, $.proxy(function(response) {
        var uids = [];
        
        if(!!response) {
        	var newName = response.url.split("/");
        	
            var data = {
                uid: response.uid,
                id: newName[newName.length-1],
                portal_type: obj.attr('data-portal-type'),
                contenttype: ('contenttype-'+obj.attr('data-portal-type').toLowerCase()),
                contenticon: obj.attr('data-contenticon'),
                url: response.url,
                imgsrc: obj.find('img:not(.loading)').attr('src'),
                title: obj.find('.item-title').text(),
                author: obj.attr('data-addinfo-author'),
                created: obj.attr('data-addinfo-date-created'),
                edited: obj.attr('data-addinfo-date-edited'),
                description: obj.attr('data-addinfo-description'),
                aclass: obj.attr('data-portal-type') == 'Folder' ? '' : 'linked-document link-overlay',
                relpb: ($('#thumbnail-view').find('div.folder-item').length+100),
            };
            
            $('#thumbnail-view form[name="folderContentsForm"]')
                .find('.folder-item')
                .each(function() {
                    $(this).show();
                });
                
            if($('#thumbnail-view form').children().length > 1) {
                $('#thumbnail-view').find('.more-item').hide();
            } else {
                $('#thumbnail-view').find('.more-item').show();
            }

            $('html, body').animate({
                //scrollTop: $('#thumbnail-view').find('.folder-item').last().offset().top
            	scrollTop: $($('#thumbnail-view').find('.folder-item').last()[0] || $('#thumbnail-view').find('.more-item')[0]).offset().top
            }, 800);
            
            
            var $more = $('#thumbnail-view').find('.more-item');
                
            var tmpCol = this.getColumns($more[0]);
            
            if($more.hasClass('list-group')) {
                tmpCol += ' list-group';
            }
            
            if(data.portal_type == 'Folder') {
                $($('#dragdrop-droppableFolder-wrapper-tmpl').render(data)).addClass(tmpCol).insertBefore('#thumbnail-view .more-item');
                //$('#dragdrop-folderitem-folder-key-tmpl').tmpl(data).insertBefore('#thumbnail-view .more-item');
            } else {
                $($('#dragdrop-droppableItem-wrapper-tmpl').render(data)).addClass(tmpCol).insertBefore('#thumbnail-view .more-item');
                //$('#dragdrop-folderitem-key-tmpl').tmpl(data).insertBefore('#thumbnail-view .more-item');
            }
                    
            
            $('.folder-item').each(function() {
                uids.push($(this).attr('id'));
            });
            $.getJSON('@@ajax-sorting', {'order': uids.join()});
            
            
            $('p#dragdrop-container').find('#'+uid).find('span.delete-item').trigger('click');
            
            
            this.thumbnailViewPrepOverlay($('#thumbnail-view').find('.folder-item').last(), data.portal_type);
            this.thumbnailViewHoverIntent();
        }
        
        var els = $('#thumbnail-view').find('.folder-item, .more-item');
        
        els.equalHeights();
    }, this));
};


DragDrop.prototype.thumbnailViewHoverIntent = function() {
    $('#thumbnail-view div.folder-item:not(.list-group) div.thumbnail').off('click', '.additional-information-trigger');
    $('#thumbnail-view div.folder-item:not(.list-group) div.thumbnail').on('click', '.additional-information-trigger', $.proxy(function(e) {
        e.preventDefault();
        
        this.toggleAdditionalInformation(e);
    }, this));
};


DragDrop.prototype.thumbnailViewPrepOverlay = function(obj, portal_type) {
    $('.linked-document').prepOverlay({
        subtype: 'ajax',
        width: '533px',
        height: '50px',
        config: {
            onLoad: $.proxy(function() {
                this.prepContentView();
            }, this)
        }
    });
    
    $('.Image').find('.linked-document').prepOverlay({
        subtype: 'ajax',
        width: "800px",
        height: "50px",
        config: {
            onLoad: $.proxy(function() {
                this.prepContentView();
            }, this)
        }
    });
};


DragDrop.prototype.mouseEventHandler = function() {
	$(document).on('click', this.dragDropContainer + ' span.delete-item', $.proxy(function(e) {
		this.removeFromDragDrop($(e.target).parents('.drag-drop-container'));
	}, this));
	
	$(document).on('click', this.dragDropContainer + ' .copy-move-item', $.proxy(function(e) {
		$target = $(e.target);
		
		if($target.parents('.drag-drop-container').find('input[type="checkbox"]').prop('checked')) {
			$('dl.portlet-static-drag-drop').find('.drag-drop-container').find('input[type="checkbox"]:checked').each($.proxy(function(k, el) {
				var state = 'move';
				// if else für copy/move
				if($('.copy-move-container').find('button.state-active').hasClass('copy')) {
					state = 'copy'
				}
					
				this.insertToThumbnailView($(el).parents('.drag-drop-container'), state);
			}, this));
		} else {
			var state = 'move';
			
			if($('.copy-move-container').find('button.state-active').hasClass('copy')) {
				state = 'copy';
			}
			
			this.insertToThumbnailView($target.parents('.drag-drop-container'), state);
		}
	}, this));
	
	$(document).on('hover', this.dragDropContainer, function(e) {
		$(this).toggleClass('state-hover');
	});
	
	$(document).on({
		click: $.proxy(function(e) {
			var $btn = $(e.target);
			
			if(!$btn.prop('disabled')) {
				if($btn.hasClass('copy')) {
					if(!$btn.hasClass('state-active')) {
						$btn.addClass('state-active').removeClass('state-hover');
						$btn.next().removeClass('state-active');
					}
				} else if($btn.hasClass('move')) {
					if(!$btn.hasClass('state-active')) {
						$btn.addClass('state-active').removeClass('state-hover');
						$btn.prev().removeClass('state-active');
					}
				}
			}
		}, this),
		hover: $.proxy(function(e) {
			var $btn = $(e.target);
			
			if(!$btn.prop('disabled') && !$btn.hasClass('state-active')) {
				$btn.toggleClass('state-hover');
			}
		}, this)
	}, 'dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar');
	
	$(document).on('click', '#thumbnail-view .toolbar .delete', $.proxy(function(e) {
		this.moveToTrash($(e.target).parents('.folder-item'), $(e.target).parents('.folder-item').attr('id'));
    }, this));
};


DragDrop.prototype.keyboardEventHandler = function() {
	var shiftDown = false,
		ctrlDown = false,
		cDown = false,
		vDown = false,
		shiftKey = 16,
		ctrlKey = 17,
		vKey = 86,
		cKey = 67,
		delKey = 46,
		backSpace = 8;
	
	$(document).on({
		keydown: $.proxy(function(e) {
			var keyCode = e.which;
			
			switch(keyCode) {
				case ctrlKey:
					ctrlDown = true;
					
					if(!shiftDown) {
						$('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar.copy').trigger('click');
					}
					break;
				case shiftKey:
					shiftDown = true;
					
					if(!$('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar.move').prop('disabled')) {
						$('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar.move').trigger('click');
					}
					break;
				case cKey:
					if(ctrlDown) {
						cDown = true;
						vDown = false;
					}
					break;
				case vKey:
					if(ctrlDown || shiftDown) {
						vDown = true;
						cDown = false;
					}
					break;
				case delKey:
				case backSpace:
					if(keyCode == delKey || (ctrlDown && keyCode == backSpace)) {
						$.getJSON('@@ajax-dragdrop', {action:'can_delete'}, $.proxy(function(response) {
							if(this.castBool(response) == true) {
								$('#thumbnail-view').find('.folder-item').find('input[type="checkbox"]:checked').each($.proxy(function(k, el) {
									this.moveToTrash($(el).parents('.folder-item'), $(el).parents('.folder-item').attr('id'));
								}, this));
							}
						}, this));
					}
					break;
			}
			
			var selEl = $('dl.portlet-static-drag-drop').find('.drag-drop-container').find('input[type="checkbox"]:checked').length <= 0 ? '' : ':checked';
			
			if(shiftDown && vDown && !cDown) {
				// move items
		        $('dl.portlet-static-drag-drop').find('.drag-drop-container').find('input[type="checkbox"]' + selEl).each($.proxy(function(k, el) {
		            this.insertToThumbnailView($(el).parents('.drag-drop-container'), 'move');
		        }, this));
			} else if(ctrlDown && !shiftDown && (cDown || vDown)) {
				if(cDown && !vDown) {
					// move to dragdrop area
		            $('#thumbnail-view').find('.folder-item').find('input[type="checkbox"]:checked').each($.proxy(function(k, el) {
		                this.droppableDrop($(el).parents('.folder-item'), $('dl.portlet-static-drag-drop'));
		            }, this));
				} else if(!cDown && vDown) {
					// copy items
		            $('dl.portlet-static-drag-drop').find('.drag-drop-container').find('input[type="checkbox"]'+selEl).each($.proxy(function(k, el) {
		                this.insertToThumbnailView($(el).parents('.drag-drop-container'), 'copy');
		            }, this));
				}
			}
		}, this),
		keyup: $.proxy(function(e) {
			var keyCode = e.which;
			
			switch(keyCode) {
				case ctrlKey:
					ctrlDown = false;
					break;
				case shiftKey:
					shiftDown = false;
					break;
				case cKey:
					cDown = false;
					break;
				case vKey:
					vDown = false;
					break;
			}
		}, this)
	});
	
	$('#thumbnail-view').on('click', function(e) {
        var $target = $(e.target);
    
        if($target.parents('.folder-item').length > 0 && shiftDown) {
            e.preventDefault();
            
            var $checkbox = $(e.target).parents('.folder-item').find('input[type="checkbox"]');
            
            if($checkbox.prop('checked') === true) {
                $checkbox.prop('checked', false).trigger('change');
            } else {
                $checkbox.prop('checked', true).trigger('change');
            }
            
            return false;
        }
    });
};


DragDrop.prototype.initEview = function() {
	var self = this;
	
	var options = {
		accept: '#thumbnail-view .folder-item',
		tolerance: 'pointer',
		over: function(event, ui) {
			var container = $(this),
				uid = ui.draggable.attr('id'),
				content_path = $.trim(container.find('span.content_path').text()),
				content_url = $.trim(container.find('span.content_url').text()),
				state = $('dl.portlet-static-drag-drop').find('.copy-move-container').find('.action-bar.state-active').hasClass('move') ? 'move' : 'copy';
			
			$.getJSON(content_url + '/@@ajax-dragdrop', {action: 'can_' + state, uid: uid}, function(response) {
				if(self.castBool(response) == true) {
					container.removeClass('state-error').addClass('state-hover');
				} else {
					container.addClass('state-error').removeClass('state-hover');
				}
			});
		},
		out: function(event, ui) {
			$('dl.portletAjaxNavigation').find('.ui-droppable').each(function() {
                $(this).removeClass('state-error state-hover');
            });
		},
		drop: function(event, ui) {
			var self = this;
			
            var container = $(this),
                uid = ui.draggable.attr('id'),
                content_path = $.trim(container.find('span.content_path').text()),
                content_url = $.trim(container.find('span.content_url').text()),
                state = $('dl.portlet-static-drag-drop').find('.copy-move-container').find('.action-bar.state-active').hasClass('move') ? 'move' : 'copy';
            
            $.getJSON('@@ajax-dragdrop', {action: 'can_' + state, uid: uid}, function(response) {
                if(self.castBool(response) == true) {
                    $.getJSON(content_url + '/@@ajax-dragdrop', {action: state + '_object', uid: uid}, function(response) {
                        container.removeClass('state-error state-hover', 250);
                        
                        if(state == 'move') {
                            ui.draggable.fadeOut(600, function() {
                                ui.draggable.remove();
                            });
                        }
                    });
                } else {
                    container.removeClass('state-error state-hover', 250);
                }
                
                container.removeClass('state-error state-hover', 250);
            });
        }
	};
    
    // init droppables
    if($('dl.portletAjaxNavigation').length > 0) {
        $('dl.portletAjaxNavigation').find('ul#subfolder_listing li').each(function() {
            if($(this).hasClass('is_folderish')) {
                $(this).droppable(options);
            }
        });
    }
};



$(document).ready(function() {
        var dnd = new DragDrop();
        // initialize dragdrop portlet
        dnd.checkPermission();
        // initialize sortable
        dnd.initSortable();
        // initialize trash portlet
        dnd.initTrash();
        // initialize dropable
        dnd.initDropable();
        // init eview
        dnd.initEview();
});
*/