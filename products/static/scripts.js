// set mastHead margin-top depending on mainNav height
$(document).ready(() => {
    var navHeight = $("#mainNav").css("height");
    $(".head").css("margin-top", navHeight);
});

// visual effect on product card hover
$(".product-card .hover-div ").mouseenter((e) => {
    $(e.target).parent().animate({
        margin: "12px"
    }, 100);
});

$(".product-card .hover-div").mouseleave((e) => {
    $(e.target).parent().animate({
        margin: "15px"
    }, 100);
});

// Navigate to product details
$(".product-card .hover-div").click((e) => {
    window.location.assign('/products/details/' + $(e.target).attr("data"));
});

// AJAX call to save a product for actual user
$(".save-div p").click((e) => {
    let pageUrl = $(e.target).attr("page-origin")
    let pageOrigin = pageUrl.match(new RegExp("[^/][a-z]+-"))[0].replace("-", "");

    console.log(pageOrigin);

    $.ajax({
        type: "GET",
        url: '/products/user-save-product/' + $(e.target).attr("data"),
        success: (data) => {
            $("#save-product-message").text("Le produit " + data['product_name'] + " a été " + data['response']);
            $("#save-product-message").show();
            setTimeout(function() { 
                $("#save-product-message").hide();
            }, 1500);
            
            if (data['saved']) {
                $(e.target).text("Retirer des favoris");
                $(e.target).css("background", "red");
            }
            else {
                if (pageOrigin == "user") {
                    $("#product-card-" + $(e.target).attr("data")).css("display", "none");
                }
                else {
                    $(e.target).text("Ajouter aux favoris");
                    $(e.target).css("background", "green");
                }
            }
        }
    });
});