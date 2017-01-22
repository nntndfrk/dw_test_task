    //$(document).ready(function() {
        this.i = 0;

        $('#progressbar').fadeOut();
        $('#tab2').fadeOut();
        $('#tab3').fadeOut();

        $('select').material_select();
        $('ul.tabs').tabs();

        $(".button-collapse").sideNav();

        var p1 = $('#date1').pickadate({
            selectMonths: true,
            selectYears: 4,
            monthsFull: [ 'січень', 'лютий', 'березень', 'квітень', 'травень', 'червень', 'липень', 'серпень', 'вересень', 'жовтень', 'листопад', 'грудень' ],
            monthsShort: [ 'січ', 'лют', 'бер', 'кві', 'тра', 'чер', 'лип', 'сер', 'вер', 'жов', 'лис', 'гру' ],
            weekdaysFull: [ 'неділя', 'понеділок', 'вівторок', 'середа', 'четвер', 'п‘ятниця', 'субота' ],
            weekdaysShort: [ 'нд', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб' ],
            today: '&nbsp'+'&nbsp'+'сьогодні',
            clear: '&nbsp'+'&nbsp'+'викреслити',
            close: 'закрити',
            firstDay: 1,
            format: 'dd mmmm yyyy',
            formatSubmit: 'dd/mm/yyyy',
            min: new Date($('input[name=datefrom]').val()),
            max: new Date($('input[name=dateto]').val())
        }).pickadate('picker');

        p1.set('select', new Date(
            $('input[name=dateto]').val()
        ));

        var p2 = $('#date2').pickadate({
            selectMonths: true,
            selectYears: 4,
            monthsFull: [ 'січень', 'лютий', 'березень', 'квітень', 'травень', 'червень', 'липень', 'серпень', 'вересень', 'жовтень', 'листопад', 'грудень' ],
            monthsShort: [ 'січ', 'лют', 'бер', 'кві', 'тра', 'чер', 'лип', 'сер', 'вер', 'жов', 'лис', 'гру' ],
            weekdaysFull: [ 'неділя', 'понеділок', 'вівторок', 'середа', 'четвер', 'п‘ятниця', 'субота' ],
            weekdaysShort: [ 'нд', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб' ],
            today: '&nbsp'+'&nbsp'+'сьогодні',
            clear: '&nbsp'+'&nbsp'+'викреслити',
            close: 'закрити',
            firstDay: 1,
            format: 'dd mmmm yyyy',
            formatSubmit: 'dd/mm/yyyy',
            min: new Date($('input[name=datefrom]').val()),
            max: new Date($('input[name=dateto]').val())
        }).pickadate('picker');

        p2.set('select', new Date(
            $('input[name=dateto]').val()
        ).valueOf()-1000*60*60*24);

    //});


    $(document).on('submit', '#leftform', function (e) {
        e.preventDefault();

        var shopsList = [];
        var categoryList = [];
        var progressBar = $('#progressbar');

        if( $('#shops :selected').length > 0 ){
            $('#shops :selected').each(function(i, selected){
                shopsList[i] = $(selected).val()
            });
        };
        if( $('#category :selected').length > 0 ){
            $('#category :selected').each(function(i, selected){
                categoryList[i] = $(selected).val()
            });
        }

        $.ajax({
            type: 'POST',
            url: '/get_main_data/',
            data: {
                shops:JSON.stringify(shopsList),
                category:JSON.stringify(categoryList),
                date1:$("#date1-field > input[name~='_submit']").val(),
                date2:$("#date2-field > input[name~='_submit']").val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },

            beforeSend: function () {
                progressBar.fadeIn();
                $('ul.tabs').tabs('select_tab', 'test1');
                $('#tab2').fadeOut();
                $('#tab3').fadeOut();
            },

            success: function(response){
              response = $.parseJSON(response);

              if (response.qty_diff !== null){

              var trHTML ='<thead>'+
                                    '<tr>'+
                                        '<th>'+'Показник'+'</th>'+
                                        '<th>'+response.date1.date+'</th>'+
                                        '<th>'+response.date2.date+'</th>'+
                                        '<th>'+'Різниця в &#37'+'</th>'+
                                        '<th>'+'Різниця'+'</th>'+
                                    '</tr>'+
                                '</thead>'+
                                '<tbody>'+
                                    '<tr>'+
                                        '<td>'+'Оборот'+'</td>'+
                                        '<td>'+response.date1.turnover.toFixed(2)+'</td>'+
                                        '<td>'+response.date2.turnover.toFixed(2)+'</td>'+
                                        '<td>'+response.turnover_diff_perc.toFixed(2)+'</td>'+
                                        '<td>'+response.turnover_diff.toFixed(2)+'</td>'+
                                    '</tr>'+
                                    '<tr>'+
                                        '<td>'+'Кількість товарів'+
                                        '<td>'+response.date1.qty.toFixed(2)+'</td>'+
                                        '<td>'+response.date2.qty.toFixed(2)+'</td>'+
                                        '<td>'+response.qty_diff_perc.toFixed(2)+'</td>'+
                                        '<td>'+response.qty_diff.toFixed(2)+'</td>'+
                                    '</tr>'+
                                    '<tr>'+
                                        '<td>'+'Кількість чеків'+'</td>'+
                                        '<td>'+response.date1.receipts_qty+'</td>'+
                                        '<td>'+response.date2.receipts_qty+'</td>'+
                                        '<td>'+response.receipts_qty_diff_perc.toFixed(2)+'</td>'+
                                        '<td>'+response.receipts_qty_diff.toFixed(2)+'</td>'+
                                    '</tr>'+
                                    '<tr>'+
                                        '<td>'+'Середній чек'+'</td>'+
                                        '<td>'+response.date1.receipts_mean.toFixed(2)+'</td>'+
                                        '<td>'+response.date2.receipts_mean.toFixed(2)+'</td>'+
                                        '<td>'+response.receipts_mean_diff_perc.toFixed(2)+'</td>'+
                                        '<td>'+response.receipts_mean_diff.toFixed(2)+'</td>'+
                                    '</tr>'+
                                '</tbody>';

              $('#main-data').empty();
              $('#main-data').append(trHTML);
              $('#tab2').fadeIn();
            } else {

                var shopsNms = [];
                var categoryNms = [];

                if( $('#shops :selected').length > 0 ){
                    $('#shops :selected').each(function(i, selected){
                        shopsNms[i] = $(selected).text();
                    });
                }
                if( $('#category :selected').length > 0 ){
                    $('#category :selected').each(function(i, selected){
                        categoryNms[i] = $(selected).text();
                    });
                }
                var now = moment(new Date());
                var er = "<div class='card-panel deep-orange lighten-5'><span><i>"+now.format("kk:mm")+"</i><br/></span>Не вдалось отримати даних" + " по магазинах: "+ (shopsNms.length > 0 ? shopsNms.join(', ') : "Shop №01, Shop №02, Shop №03") + ", в таких категоріях: " + (categoryNms.length > 0 ? categoryNms.join(', ') : "всі") + "</div>";
                $('#main-data-msg').after(er);

            }

            }
        });
        $.ajax({
            type: 'POST',
            url: '/get_prod_data/',
            data: {
                shops:JSON.stringify(shopsList),
                category:JSON.stringify(categoryList),
                date1:$("#date1-field > input[name~='_submit']").val(),
                date2:$("#date2-field > input[name~='_submit']").val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },

            complete: function () {
                progressBar.fadeOut();
            },

            success: function(resp){
              $('#test4').empty();
              resp = $.parseJSON(resp);

              if (typeof resp.increased_prod != "undefined" && resp.increased_prod.length > 0) {
                // if (resp.increased_prod && resp.decreased_prod) alert('pisun!');
                $('#prod-data1').empty();
                var trHTML1 = '<p class="flow-text">Товари, які виросли в продажах</p><table id="prod-data1" class="responsive-table"><thead>'+'<tr>'+'<th>'+'Назва товару'+'</th>'+'<th>'+'Зміна кількості продаж'+'</th>'+'<th>'+'Зміна обороту'+'</th>'+'</tr>'+'</thead>'+'<tbody>';
                $.each(resp.increased_prod, function(i, item){
                trHTML1 += '<tr>'+'<td>'+ (item.index ? item.index : item.name )+'</td>'+'<td>'+item.qty_diff.toFixed(2)+'</td>'+'<td>'+item.turn_diff.toFixed(2)+'</td>'+'</tr>';
              });
                trHTML1+='</tbody></table>';
                $('#test4').append(trHTML1);
                };
              if (typeof resp.decreased_prod != "undefined" && resp.decreased_prod.length > 0) {
                $('#prod-data2').empty();
                var trHTML2 = '<p class="flow-text">Товари, які впали в продажах</p><table id="prod-data2" class="responsive-table">'+'<thead>'+'<tr>'+'<th>'+'Назва товару'+'</th>'+'<th>'+'Зміна кількості продаж'+'</th>'+'<th>'+'Зміна обороту'+'</th>'+'</tr>'+'</thead>'+'<tbody>';
                $.each(resp.decreased_prod, function(i, item){
                    trHTML2 += '<tr>'+'<td>'+(item.index ? item.index : item.name )+'</td>'+'<td>'+item.qty_diff.toFixed(2)+'</td>'+'<td>'+item.turn_diff.toFixed(2)+'</td>'+'</tr>';
                });
                trHTML2+='</tbody></table>';
                $('#test4').append(trHTML2);

              };

            if ( (typeof resp.increased_prod != "undefined" && resp.increased_prod.length > 0) || (typeof resp.decreased_prod != "undefined" && resp.decreased_prod.length > 0)) {$('#tab3').fadeIn();}

            }
        });
    });