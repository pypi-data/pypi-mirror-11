function AjustarSeriesAConteo(attrs){

  var loginventario_id = attrs.loginventario_id
  var salida_id = attrs.salida_id
  var entrada_id = attrs.entrada_id
  var onSuccess = attrs.onSuccess

  $.ajax({
    url:'/inventarios/inventarios_fisicos/ajustar_seriesinventario/', 
    type : 'get', 
    data:{
      'loginventario_id':loginventario_id,
      'salida_id':salida_id,
      'entrada_id':entrada_id,
    }, 
    success: function(data){
      onSuccess()
    },
    error: function() {
    },
  })
}




function cerrar_inventario(){

  var loginventario_id = $("#id_loginventario").val()
  var salida_id = $("#hidden_salida_id").val()
  var entrada_id = $("#hidden_entrada_id").val()

  function CerrarInventario(){
    $.ajax({
      url:'/inventarios/close_inventario_byalmacen_view/', 
      type : 'get', 
      data:{
        'almacen_id' : $("#almacen_id").val(),
      }, 
      success: function(data){ 
        alert(data.mensaje);
        window.location = "/inventarios/almacenes/";
      },
      error: function() {
        },
    });  
  }
  
  AjustarSeriesAConteo({
    loginventario_id: loginventario_id, 
    salida_id: salida_id,
    entrada_id: entrada_id,
    onSuccess: CerrarInventario,
  })

  // CerrarInventario()
  
  
}

function AgregarArticuloSinExistencia(args){
  var $triggerBtn = args.$triggerBtn
  var $triggerBtnByLine = args.$triggerBtnByLine

  mostrar_articulos_agregados = function(data){
    if (data.articulos_agregados > 0)
    {
      mensaje ='Se agregaron '+ data.articulos_agregados+ ' Articulos'
      if (data.articulo_pendientes > 0)
        mensaje = 'La aplicacion solo genero ' + data.articulos_agregados+ ' Articulos, faltaron de generar '+data.articulo_pendientes + ' Articulos.'
      alert(mensaje)
    }
    else
    {
      if (data.message != '')
        alert(data.message);
      else
        alert('No hay articulos por inicializar');
    }

    // limpiar formulario para agregar articulos
    $("#id_agregando_span, #id_agregando_span_all").attr("class","hide")
    $triggerBtn.show()
    $triggerBtn.attr("disabled",false)
  }

  AddArticles = function(attrs){
    var line = null
    if (attrs != undefined) {
      line = attrs.line
    }

    if ( $triggerBtn.attr("disabled") == "disabled")
      return false

    $triggerBtn.hide();
    $triggerBtn.attr("disabled",true);
    $("#btnCancel").hide()
    $("#id_agregando_span, #id_agregando_span_all").attr("class","")


    if (line == undefined) {
      $.ajax({
        url:'/inventarios/add_articulossinexistencia/', 
        type : 'get', 
        data:{
          'almacen_id' : $("#almacen_id").val(),
        }, 
        success: function(data){ 
          mostrar_articulos_agregados(data)
          $("#articulosnocont_porlinea_Modal, #articulosnocont_Modal").modal("hide")
          $("#btnCancel").show()
        },
        error: function() {
          alert('fallo algo')
        },
      }); 
    }else{
      $.ajax({
        url:'/inventarios/add_articulossinexistencia_bylinea/', 
        type : 'get', 
        data:{
          'almacen_id' : $("#almacen_id").val(),
          'linea_id': line,
          'ubicacion': $("#ubicacion").val(),
        }, 
        success: function(data){ 
          mostrar_articulos_agregados(data)
          $("#articulosnocont_porlinea_Modal, #articulosnocont_Modal").modal("hide")
          $("#btnCancel").show()
        },
        error: function() {
          alert('fallo algo')
        },
      }); 
    }
  }


  $triggerBtn.on("click", function(){
    AddArticles()
  })

  $triggerBtnByLine.on('click', function(){
    AddArticles({
      line: $("#id_linea").val()
    })
  })


}

AgregarArticuloSinExistencia({
  $triggerBtn: $("#btn_agregar_articulosinexistencia"),
  $triggerBtnByLine: $("#btn_agregar_articulosinexistencia_bylinea"),
})
