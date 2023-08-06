/**
 * DateTimeDirect widget JS
 */

$(document).ready(function() {
    $.fn.changeradiofunction = function(){
        $("#id_publish_from_date").attr("disabled", false);
        $("#id_publish_from_time").attr("disabled", false);
    }

    if ($("#id_publish_from_date").val() || $("#id_publish_from_time").val()) {
        $("#notdirect").attr("checked", "checked");
        $.fn.changeradiofunction();
    }

    if($('#notdirect').is(':checked')) {
        $.fn.changeradiofunction()
    }

    $('#direct').change( function () {
        $("#id_publish_from_date").attr("disabled", true);
        $("#id_publish_from_date").attr("value", "");
        $("#id_publish_from_time").attr("disabled", true);
        $("#id_publish_from_time").attr("value", "");
    });

    $('#notdirect').change( function () {
        $("#id_publish_from_date").attr("disabled", false);
        $("#id_publish_from_time").attr("disabled", false);
    });

});
