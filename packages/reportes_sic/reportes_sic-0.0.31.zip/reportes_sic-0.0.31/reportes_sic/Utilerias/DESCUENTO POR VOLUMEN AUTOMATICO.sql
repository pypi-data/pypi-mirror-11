CREATE OR ALTER trigger sic_dsctos_vol_max for doctos_pv_det
active before insert or update position 1
AS
declare variable unidades_articulo double precision;
declare variable unidades_minimas double precision;
declare variable pctje_dscto_vol double precision;
declare variable total_dscto_dinero_pol double precision;
declare variable dinero_descuentos_aplicados double precision;
declare variable dscto_dinero_detalle double precision;
declare variable dscto_a_aplicar double precision;

declare variable detalle_unidades double precision;
declare variable detalle_precio double precision;
declare variable detalle_porcentaje_desc double precision;
declare variable descuento_porcentaje double precision;
declare variable existe_count integer;
begin
  select count(*) from dsctos_vol_arts dvo join  politicas_dsctos_volumen pvo on pvo.politica_dscto_volumen_id = dvo.politica_dscto_volumen_id
       where pvo.nombre = 'SIC_VOLUMEN' and dvo.articulo_id = new.articulo_id into :existe_count;
  if (existe_count is null) then
    existe_count = 0;
  if(existe_count > 0) then
   begin
        /* REGRESA LAS UNIDADES Y EL PORCENTAJE DE DESCUENTO A APLICAR EN CADA CASO */
        select dvo.unidades, dvo.descuento from dsctos_vol_arts dvo join politicas_dsctos_volumen pvo on pvo.politica_dscto_volumen_id = dvo.politica_dscto_volumen_id
        where pvo.nombre = 'SIC_VOLUMEN' and dvo.articulo_id = new.articulo_id AND DVO.descuento > 0 into :unidades_minimas, :pctje_dscto_vol;

        /* SE OBTIENE LA CANTIDAD DE UNIDADES DEL MISMO ARTICULO EN LOS DEMAS DETALLES DEL DOCUMENTO */
        select sum(unidades) from doctos_pv_det dpd where dpd.articulo_id = new.articulo_id and dpd.docto_pv_id = new.docto_pv_id
        and dpd.docto_pv_det_id <> new.docto_pv_det_id into :unidades_articulo;

        if (dinero_descuentos_aplicados is null) then
          dinero_descuentos_aplicados = 0;

        For SELECT dpd.unidades, dpd.precio_unitario, dpd.pctje_dscto from doctos_pv_det dpd where dpd.articulo_id = new.articulo_id and dpd.docto_pv_id = new.docto_pv_id
        and dpd.docto_pv_det_id <> new.docto_pv_det_id into :detalle_unidades, :detalle_precio, :detalle_porcentaje_desc
        do
        begin
             dinero_descuentos_aplicados = dinero_descuentos_aplicados +  (detalle_unidades * detalle_precio * detalle_porcentaje_desc /100);
        end

        if (unidades_articulo is null) then
          unidades_articulo = 0;

        total_dscto_dinero_pol = unidades_minimas * new.precio_unitario * (pctje_dscto_vol/100);

        if (unidades_articulo+new.unidades >= unidades_minimas) then
            dscto_a_aplicar = total_dscto_dinero_pol;
        else
            dscto_a_aplicar =  (unidades_articulo + new.unidades) * new.precio_unitario * (pctje_dscto_vol/100);

        dscto_dinero_detalle = dscto_a_aplicar - dinero_descuentos_aplicados;
        descuento_porcentaje = dscto_dinero_detalle * 100 / (new.unidades * new.precio_unitario);
        if (descuento_porcentaje < 0) then
            new.pctje_dscto = 0 ;
        else
            new.pctje_dscto = descuento_porcentaje;
        
   end
end

@

CREATE OR ALTER trigger sic_dsctos_vol_max_cobro for doctos_pv_cobros
active before insert or update position 0
AS
declare variable articulo_id integer;
declare variable dscto_a_aplicar double precision;
declare variable unidades_minimas double precision;
declare variable pctje_dscto_vol double precision;
declare variable unidades_articulo double precision;
declare variable precio_unitario double precision;
declare variable precio_unitario_promedio double precision;
declare variable nombre_articulo varchar(100);
declare variable posiciones varchar(20);

declare variable detalle_unidades double precision;
declare variable detalle_precio double precision;
declare variable detalle_porcentaje_desc double precision;
declare variable dinero_descuentos_aplicados double precision;

begin
    for select distinct dpd.articulo_id from doctos_pv_det dpd join dsctos_vol_arts dva on dva.articulo_id = dpd.articulo_id
        join politicas_dsctos_volumen pvo on pvo.politica_dscto_volumen_id = dva.politica_dscto_volumen_id
        where pvo.nombre = 'SIC_VOLUMEN' and dpd.docto_pv_id = new.docto_pv_id INTO :articulo_id
    do
    begin
        /* REGRESA LAS UNIDADES Y EL PORCENTAJE DE DESCUENTO A APLICAR EN CADA CASO */
        select dvo.unidades, dvo.descuento from dsctos_vol_arts dvo join politicas_dsctos_volumen pvo on pvo.politica_dscto_volumen_id = dvo.politica_dscto_volumen_id
        where pvo.nombre = 'SIC_VOLUMEN' and dvo.articulo_id = :articulo_id AND DVO.descuento > 0 into :unidades_minimas, :pctje_dscto_vol;
        /* SE OBTIENE LA CANTIDAD DE UNIDADES DEL MISMO ARTICULO EN LOS DEMAS DETALLES DEL DOCUMENTO */
        select sum(unidades) from doctos_pv_det dpd where dpd.articulo_id = :articulo_id and dpd.docto_pv_id = new.docto_pv_id into :unidades_articulo;

        /*SE OBTIENE EL PRECIO UNITARIO DEL ARTICULO EN LOS DETALLES*/
        select first 1 precio_unitario from doctos_pv_det dpd where dpd.articulo_id = :articulo_id and dpd.docto_pv_id = new.docto_pv_id into :precio_unitario;

        /* SE OBTIENE EL PROMEDIO DE PRECIOS UNITARIOS */
        select avg(precio_unitario) from doctos_pv_det dpd where dpd.articulo_id = :articulo_id and dpd.docto_pv_id = new.docto_pv_id into :precio_unitario_promedio;

        if (precio_unitario <> precio_unitario_promedio) then
            exception ex_saldo_cargo_excedido;

        if (unidades_articulo >= unidades_minimas) then
            dscto_a_aplicar = unidades_minimas * precio_unitario * (pctje_dscto_vol/100);
        else
            dscto_a_aplicar = unidades_articulo * precio_unitario * (pctje_dscto_vol/100);

        dinero_descuentos_aplicados = 0;
        /* SE OBTIENE EL TOTAL DEL DESCUENTO APLICADO EN ESE ARTICULO */
        For SELECT dpd.unidades, dpd.precio_unitario, dpd.pctje_dscto from doctos_pv_det dpd where dpd.articulo_id = :articulo_id and dpd.docto_pv_id = new.docto_pv_id
        into :detalle_unidades, :detalle_precio, :detalle_porcentaje_desc
        do
        begin
             dinero_descuentos_aplicados = dinero_descuentos_aplicados +  (detalle_unidades * detalle_precio * detalle_porcentaje_desc /100);
        end

        if (abs(dinero_descuentos_aplicados - dscto_a_aplicar)>0.1) then
        begin
            select min(nombre), cast(list(posicion) as varchar(20)) from doctos_pv_det dpd join articulos a on a.articulo_id = dpd.articulo_id
            where dpd.docto_pv_id = new.docto_pv_id and dpd.articulo_id = :articulo_id into nombre_articulo, :posiciones;
            exception ex_sic_dscto_vol 'FAVOR DE RECAPTURAR LOS DETALLES DEL SIGUIENTE ARTICULO: '|| nombre_articulo||' Posiciones: '||posiciones;
        end

    end
end
