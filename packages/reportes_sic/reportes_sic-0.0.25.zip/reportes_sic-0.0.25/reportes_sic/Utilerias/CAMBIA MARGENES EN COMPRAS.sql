CREATE OR ALTER trigger SIC_MARGENAUTO_DOCTOS_CM_DET for doctos_cm_det
active after update position 0
AS
declare variable precio numeric(18,6);
declare variable margen_nuevo numeric(18,6);

declare variable precio_articulo_id integer;
declare variable precio_articulo_moneda_id integer;
declare variable moneda_local_id integer;

declare variable precio_unitario_neto numeric(18,6);

declare variable documento_tipo char(1);
declare variable documento_tipocambio numeric(18,6);
declare variable documento_estado char(1);
declare variable documento_moneda_id integer;
declare variable documento_fecha date;

begin
    /* 04/02/2014 */
    select tipo_docto, estatus, tipo_cambio, moneda_id, fecha from doctos_cm where docto_cm_id = new.docto_cm_id
    into :documento_tipo, :documento_estado, :documento_tipocambio, :documento_moneda_id, :documento_fecha;

    if (:documento_tipo= 'C' and :documento_estado = 'N' and new.precio_total_neto <> 0 ) then
    begin
        select moneda_id from monedas where es_moneda_local='S' into :moneda_local_id;

        /* Se optiene precio_articulo_id, precio y moneda de cada lista de precios del articulo */
        for select precio_articulo_id, precio, moneda_id from precios_articulos
        where articulo_id = new.articulo_id
        into :precio_articulo_id ,:precio, :precio_articulo_moneda_id
        do
        begin
            /* Sacamos precio con descuento */
            precio_unitario_neto = new.precio_total_neto / new.unidades;
            
            /* Si el moneda de el precio no es local
            sacamos precio en moneda del precio articulo*/

            if (:precio_articulo_moneda_id <> :moneda_local_id) then
            begin
                /*Si la moneda del documento es moneda local
                sacamos precio en moneda del precio de lista segun el tipo de cambio de la fecha del documento */
                if (:documento_moneda_id = :moneda_local_id) then
                begin
                    select precio_unitario from convierte_precio_unit_s(:precio_unitario_neto, :documento_moneda_id, :documento_fecha, :precio_articulo_moneda_id, 'n', 'n') into :precio_unitario_neto;
                end
                else
                begin
                    precio_unitario_neto = :precio_unitario_neto / :documento_tipocambio;
                end
            end
            if (:precio_unitario_neto <= 0) then
            begin
                margen_nuevo = 0;
            end
            else
            begin
                /* Calculamos el nuevo margen */
                margen_nuevo =((:precio / :precio_unitario_neto )-1)*100;

            end

            if (:margen_nuevo < 0) then
            begin
               margen_nuevo = 0;
            end

            if (:margen_nuevo > 999) then
            begin
                margen_nuevo = 999;
            end

            update precios_articulos set margen=:margen_nuevo where precio_articulo_id = :precio_articulo_id;
        end
    end
end
