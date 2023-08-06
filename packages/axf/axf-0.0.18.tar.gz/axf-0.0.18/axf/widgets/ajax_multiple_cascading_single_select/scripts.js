
var AjaxMultipleCascadingSingleSelectField_init = function(field, fields, datasource, value) {

    var Jfields = [];
    for (var i = 0; i < fields.length; i++){
        Jfields[i] = jQuery(fields[i]);
    }
    var selected_value = value;

    for (var j = 0; j<fields.length; j++){
        Jfields[j].change(function(){
            var selected = [];
            for (var i = 0; i<fields.length; i++){
                selected[i] = Jfields[i].val();
            }
            jQuery.getJSON(datasource, {val: JSON.stringify(selected)}, function(resp){
                var opts = resp.options;
                var options = '';
                for (var i = 0; i < opts.length; i++) {
                    console.log(selected_value);

                    if (opts[i].value == selected_value){
                        options += '<option value="' + opts[i].value + '" selected="true">' + opts[i].name + '</option>';
                        selected_value = '';
                    }
                    else
                        options += '<option value="' + opts[i].value + '">' + opts[i].name + '</option>';
                }
                jQuery(field).html(options).change();
                });
            });

    }
};