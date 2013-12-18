$("a[rel^='chg']").click(function (event) {
    event.preventDefault();
    var addr = $(this).attr("name").split('/');
    var t = 'form[id="'+addr[0]+'"]';
    var data = $(t).serialize();
    var action = confirm('Вы уверены, что желаете внести изменения?');
    var path = location.host;
    if(action){
        console.log("here");
        $.post( "//"+path+"/switches/", data, function() {
            $("#content").text("Загружаю...");
            $("#content").load("//"+path+"/switches/"+addr[1]+'/'+addr[2]+'/');
        });
    }
});

$("input[id='portstatus']").change(function (event) {
    var n = ($(this).attr("name")).split(":");
    var path = location.host;
    console.log(n[0]);
    if (this.checked){
        var data = "sw="+n[0]+"&port="+n[1]+"&act=open";
    }
    else {
        var data = "sw="+n[0]+"&port="+n[1]+"&act=close";
    }
    $.get( "//"+path+"/portaction/", data, function() {
        $("#content").text("Загружаю...");
        $("#content").load("//"+path+"/switches/"+n[2]+'/'+n[3]+'/');
    });
});

    $("input[id='trust']").change(function (event) {
        var n = ($(this).attr("name")).split(":");
        var path = location.host;
        if (this.checked){
            var data = "sw="+n[0]+"&port="+n[1]+"&act=check";
        }
        else {
            var data = "sw="+n[0]+"&port="+n[1]+"&act=uncheck";
        }
        $.get( "//"+path+"/trustaction/", data, function() {
            $("#content").text("Загружаю...");
            $("#content").load("//"+path+"/clients/"+n[2]+'/'+n[3]+'/');
        });
    });