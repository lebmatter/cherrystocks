$(document).ready(function () {

    var $containerdiv = $('#cardwrap');
    function populate_cards(gtype){
            $.get("/niftyfifty?type="+gtype, function (data) {
        console.log(data);

        $(".gtype").css('border-bottom', 'none');
        $("#"+gtype).css('border-bottom', '1px dashed white');

        var parsed_data = JSON.parse(data);
        var entries = parsed_data['data'];
        var tstamp = parsed_data['tstamp'];
        $('#tstamp').text(tstamp);
        $containerdiv.html('');
        $.each(entries, function (index, value) {
            var $cdiv = $("<div>", {
                "class": "card"
            });
            var $ctop = $("<div>", {
                "class": "card-top"
            });
            var $cfooter = $("<div>", {
                "class": "card-footer"
            });
            var $symbol = $("<p>").text(value['symbol']);
            $ctop.append($symbol);
            var $cfooterl = $("<div>", {
                "class": "card-footer-div"
            });
            var $cfooterr = $("<div>", {
                "class": "card-footer-div"
            });
            $cfooterl.append(
                '<div class="valtext">LTP ' + value['ltp'] + '</div>'
            ).append(
                '<div class="valtext">OPEN ' + value['openPrice'] + '</div>'
            ).append(
                '<div class="valtext">PREV ' + value['previousPrice'] + '</div>'
            );
            $cfooterr.append('<span class="netprice '+gtype+'">' + value['netPrice'] + '%</span>')
            var $cfooter2 = $("<div>", {
                "class": "card-footer2"
            });
            $cfooter2.append(
                    '<div class="valtext">LOW '+value['lowPrice']+' - '+value['highPrice']+' HIGH</div>'
                ).append(
                    '<div class="valtext">TRADE QTY '+value['tradedQuantity']+' | TURNOVER '+value['turnoverInLakhs']+' </div>'
                )
            $cdiv.append($ctop);
            $cfooter.append($cfooterl).append($cfooterr);
            $cdiv.append($cfooter);
            $cdiv.append($cfooter2);

            $containerdiv.append($cdiv);
        });

    });
    } //function

    /* Call on page load */
    populate_cards('gainers');

    $(".gtype").click(function(){
        var gtype = $(this).attr('id');
        populate_cards(gtype);
    });
});