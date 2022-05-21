
!function($) {
    "use strict";

    var SweetAlert = function() {};

    //examples 
    SweetAlert.prototype.init = function() {
        
    //Auto Close Timer
    $('#sa-close').click(function(){
         swal({   
            title: "Existoso",   
            text: "Factura Electrónica Creada Correctamente.",   
            type: "success",
            timer: 2000,   
            showConfirmButton: false 
        });
    });

    $('#sa-pos').click(function(){
         swal({   
            title: "Existoso",   
            text: "Factura POS Creada Correctamente.",   
            type: "success",
            timer: 2000,   
            showConfirmButton: false 
        });
    });

    $('#update_success').click(function(){
         swal({   
            title: "Existoso",   
            text: "Actualización Exitosa.",   
            type: "success",
            timer: 1700,   
            showConfirmButton: false 
        });
    });

    $('#add_success').click(function(){
         swal({   
            title: "Existoso",   
            text: "Producto registrado con exito.",   
            type: "success",
            timer: 1700,   
            showConfirmButton: false 
        });
         $("#code").focus()
    });

    $('#client_select').click(function(){
         swal({   
            title: "Error",   
            text: "Debe elejir un cliente.",
            type: "error", 
            timer: 1700,   
            showConfirmButton: false 
        });
    });

    $('#fp_select').click(function(){
         swal({   
            title: "Error",   
            text: "Debe elejir una forma de págo.",
            type: "error",  
            timer: 1700,   
            showConfirmButton: false 
        });
    });
    $('#error_invoice').click(function(){
         swal({   
            title: "Error",   
            text: "La factura no fue creada.",
            type: "error",  
            timer: 2000,   
            showConfirmButton: false 
        });
    });
    $('#block_company').click(function(){
         swal({   
            title: "Error",   
            text: "Empresa bloqueada por falta de pago.",
            type: "error",  
            timer: 2000,   
            showConfirmButton: false 
        });
    });

    $('#block_empleoyee').click(function(){
         swal({   
            title: "Error",   
            text: "Empleado bloqueado.",
            type: "error",  
            timer: 2000,   
            showConfirmButton: false 
        });
    });

    $('#less_stock').click(function(){
         swal({   
            title: "Error",   
            text: "El producto esta agotado",
            type: "error",  
            timer: 2000,   
            showConfirmButton: false 
        });
    });

    $('#register_client').click(function(){
         swal({   
            title: "Éxito",   
            text: "El cliente se registro con éxito",
            type: "success",  
            timer: 1700,   
            showConfirmButton: false 
        });
    });

    $('#register_client_error').click(function(){
         swal({   
            title: "Error",   
            text: "El cliente no registro con éxito",
            type: "error",  
            timer: 2000,   
            showConfirmButton: false 
        });
    });

    $('#email_client_error').click(function(){
         swal({   
            title: "Error",   
            text: "El E-mail no es valido",
            type: "error",  
            timer: 2000,   
            showConfirmButton: false 
        });
    });

    $('#phone_client_error').click(function(){
         swal({   
            title: "Error",   
            text: "El teléfono no es valido. Debe tener entre 7 y 10 digitos",
            type: "error",  
            timer: 2500,   
            showConfirmButton: false 
        });
    });

    $('#data_client_error').click(function(){
         swal({   
            title: "Error",   
            text: "Los datos del cliente no son validos",
            type: "error",  
            timer: 2500,   
            showConfirmButton: false 
        });
    });

    $('#error_agotado').click(function(){
         swal({   
            title: "Error",   
            text: "Producto Agotado",
            type: "error",  
            timer: 1000,   
            showConfirmButton: false 
        });
    });

    $('#error_pdf').click(function(){
         swal({   
            title: "¡ERROR!",   
            text: "Documento no valido",
            type: "error",  
            timer: 1400,   
            showConfirmButton: false 
        });
    });

    $('#resolution_expires').click(function(){
         swal({   
            title: "¡ALERTA!",   
            text: "La resolucion esta venciendo",
            type: "warning",  
            timer: 2500,   
            showConfirmButton: false 
        });
    });

    $('#resolution_expired').click(function(){
         swal({   
            title: "¡ALERTA!",   
            text: "La resolucion esta vencida",
            type: "warning",  
            timer: 2500,   
            showConfirmButton: false 
        });
    });

    $('#certificate_expires').click(function(){
         swal({   
            title: "¡ALERTA!",   
            text: "El certificado digital esta venciendo",
            type: "warning",  
            timer: 2500,   
            showConfirmButton: false 
        });
    });

    $('#certificate_expired').click(function(){
         swal({   
            title: "¡ALERTA!",   
            text: "El certificado digital esta vencido",
            type: "warning",  
            timer: 2500,   
            showConfirmButton: false 
        });
    });

    $('#transfer_inventory').click(function(){
         swal({   
            title: "¡INFORMACIÓN!",   
            text: "El inventario se esta pasando, en unos minutos el inventario de tu tienda estara listo.",
            type: "info",  
            timer: 3000,   
            showConfirmButton: false 
        });
    });

    $('#send_payroll').click(function(){
         swal({   
            title: "¡EXITOSO!",   
            text: "La nomina se esta enviando a la DIAN, cuando termine el envio le estaremos avisando!\nQue tenga un buen dia!",
            type: "success",  
            timer: 3000,   
            showConfirmButton: false 
        });
    });

    


    },
    //init
    $.SweetAlert = new SweetAlert, $.SweetAlert.Constructor = SweetAlert
}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.SweetAlert.init()
}(window.jQuery);