$(function() {
	if($("#thumbnail-viewlet").html() != null) {
		$.getJSON($("#document_path").text() + "/@@ajax-get-thumbnail", {"size" : "large"}, function(data) {
			if(data) {
				$("#thumbnail-viewlet").find(".thumbnail").attr("src", data);
			}
		});
	}
	
	//$('[class*="contenttype"]').each(function() {
		//getThumbnailUrl($(this));
	//});
	
	function getThumbnailUrl(obj) {
		var url = obj.attr('href');
		var urlSplit = url.split('/');
		
		if(urlSplit[urlSplit.length-1] == 'view') {
			url = url.substring(0, url.length - 5);
		}
		
		$.getJSON(url + '/@@ajax-get-thumbnail', {size: 'listing'}, function(data) {
			if(data) {
				obj.removeClass();
				obj.parent().find('img').detach();
				obj.prepend('<img src="' + data + '"/>');
			}
		});
	}
});
