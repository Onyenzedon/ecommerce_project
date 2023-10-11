$(document).ready(function() {
    $(".add-to-cart-btn").click(function(){
        var product_id = $(this).data("product-id")
        var product_name = $(this).data("product-name")

        console.log("Product name: ", product_name)

    alert(`Product ${product_name} of ID ${product_id} added to cart`)
    })
})