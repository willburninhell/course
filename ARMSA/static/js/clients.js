    $("input[id='portstatus']").change(function (event) {
        var n = ($(this).attr("name")).split(":");
        if (this.checked){
            var data = "sw="+n[0]+"&port="+n[1]+"&act=open";
            $.get( "//127.0.0.1:8000/portaction/", data, function() {
                $("#content").load("//127.0.0.1:8000/clients/"+n[2]+'/'+n[3]+'/');
            });
        }
        else {
            var data = "sw="+n[0]+"&port="+n[1]+"&act=close";
            $.get( "//127.0.0.1:8000/portaction/", data, function() {
                $("#content").load("//127.0.0.1:8000/clients/"+n[2]+'/'+n[3]+'/');
            });
        }
    });