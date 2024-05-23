console.log("working fine");



$("#commentForm").submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function (res) {
            console.log("comment save to DB.....");

            if (res.bool == true) {
                $("#review-res").html("Review added successfuly.")
                $(".hide-comment-form").hide()
                $(".submit-review").hide()

                let _html = '<div class="reviews_area">'
                _html += '<ul>'
                _html += '<li>'
                _html += '<div class="single_user_review mb-15">'
                _html += '<div class="review-rating">'
                _html += '{{r.rating}}'
                _html += '</div>'
                _html += '<div class="review-details">'
                _html += '<a href="#">' + res.context.user + '</a>'
                _html += '</div>'

                _html += '<div class="review-details">'
                _html += '<span>{{r.date|date:"d M,Y"}}</span>'
                _html += '</div>'

                for (let i = 1; i < res.context.rating; i++) {
                    _html += '<i class="fas fa-star text-warning">'
                }

                _html += '<p class="mb-10">' + res.context.review + '</p>'

                _html += '</div>'
                _html += '</li>'
                _html += '</ul>'
                _html += '</div>'
            }
        }
    })
})


$(document).ready(function () {
    $(".filter-checkbox, #price-filter-btn").on("click", function() {
        console.log("heyy its work..");
        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
                return element.value
            })
        })
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType: 'JSON',
            beforeSend: function () {
                console.log("sending data...");
            },
            success: function (response) {
                console.log(response);
                console.log("product filterd successfully....");
                $("#filtered-product").html(response.context)
            }
        })
    })

    $("#max_price").on("blur", function() {
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()


        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert("Price must between" + min_price + 'and' + max_price)
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()
            return false

        }
    })

    $(".add-to-cart-btn").on("click", function() {

        let this_val = $(this)
        let index = this_val.data('index');


        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()

        console.log("quantity", quantity);
        console.log("PT", product_title);
        console.log("PI", product_id);
        console.log("PP", product_price);
        console.log("PP", product_pid);
        console.log("Pi", product_image);
        console.log("Pin", index);
        console.log("CE", this_val);


        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding Product");
            },
            success: function (response) {
                this_val.html("✔");
                console.log("Added Product");
                $(".cart-items-count").text(response.totalcartitems);
            }
        });
    })

    $(".delete-product").on("click", function() {
        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("product", product_id);

        $.ajax({
            url:"/delete-from-cart",
            data:{
                "id":product_id
            },
            dataType:"json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

    $(".update-product").on("click", function() {
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-"+product_id).val()

        console.log("product", product_id);
        console.log("product", product_quantity);

        $.ajax({
            url:"/update-cart",
            data:{
                "id":product_id,
                "qty":product_quantity,
            },
            dataType:"json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })


    $(document).on("click", ".make-default-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("id is:", id);
        console.log("element is:", this_val);

        $.ajax({
            url: "/make-default-address",
            data:{
                "id":id
            },
            dataType: "json",
            success: function(response){
                console.log("address made default...");
            }
        })
    })
})




