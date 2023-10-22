$(document).ready(()=>{
    $("#id_new_categoria").css("display","none")
    $("label[for='id_new_categoria'").css("display","none")
    $("#id_new_fornecedor").css("display","none")
    $("label[for='id_new_fornecedor']").css("display","none")
    // $("#id_new_fornecedor").css("display","none")
    $("#cadastro-form").on("change",function(){
        if ($("#id_radio_button_categoria_1").is(":checked")){
            $("#id_new_categoria").css("display","none")
            $("label[for='id_new_categoria'").css("display","none")

            $("label[for='id_categoria'").css("display","block")
            $("#id_categoria").css("display","block")
        }else{
            $("#id_new_categoria").css("display","block")
            $("label[for='id_new_categoria'").css("display","block")

            $("label[for='id_categoria']").css("display","none")
            $("#id_categoria").css("display","none")
        }
        
        if ($("#id_radio_button_fornecedor_1").is(":checked")){
            $("#id_new_fornecedor").css("display","none")
            $("label[for='id_new_fornecedor']").css("display","none")

            $("label[for='id_fornecedor']").css("display","block")
            $("#id_fornecedor").css("display","block")

        }else{
            $("#id_new_fornecedor").css("display","block")
            $("label[for='id_new_fornecedor']").css("display","block")

            $("label[for='id_fornecedor']").css("display","none")
            $("#id_fornecedor").css("display","none")
        }
    })
    
})