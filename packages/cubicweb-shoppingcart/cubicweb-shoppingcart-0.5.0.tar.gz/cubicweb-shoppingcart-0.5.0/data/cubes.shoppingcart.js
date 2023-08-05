
var itemeid = 1;

function addItemInCart(carteid) {
    var d = asyncRemoteExec('add_item_in_cart', itemeid, carteid);
    d.addCallback(function (response) {
	jQuery('#cartitemstable').append(getDomFromResponse(response));
	itemeid += 1;
    });
}

function removeItemFromCart(itemeid) {
    jQuery('#cartitem' + itemeid).remove();
}
