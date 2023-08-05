CREATE OR ALTER TRIGGER SIC_EVITA_BORRAR_COMODIN FOR DOCTOS_PV_DET
ACTIVE BEFORE UPDATE POSITION 0
AS
declare variable linea varchar(50);
begin
    if (updating and old.precio_unitario_impto>0) then
        select l.nombre from articulos a join lineas_articulos l on l.linea_articulo_id = a.linea_articulo_id where a.articulo_id = new.articulo_id into :linea;
        if (linea = 'COMODINES') then
            new.precio_unitario_impto =  old.precio_unitario_impto;
end