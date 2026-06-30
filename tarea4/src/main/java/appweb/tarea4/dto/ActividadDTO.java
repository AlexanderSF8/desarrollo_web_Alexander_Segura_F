package appweb.tarea4.dto;

public class ActividadDTO {
    private Integer id;
    private String miembroNombre;
    private Integer dia;
    private String tipo;
    private String comuna;
    private String descripcion;
    private String nota; // Es String para poder enviar el "-" si no hay notas

    // Constructor vacío
    public ActividadDTO() {}

    // Getters y Setters
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getMiembroNombre() { return miembroNombre; }
    public void setMiembroNombre(String miembroNombre) { this.miembroNombre = miembroNombre; }
    public Integer getDia() { return dia; }
    public void setDia(Integer dia) { this.dia = dia; }
    public String getTipo() { return tipo; }
    public void setTipo(String tipo) { this.tipo = tipo; }
    public String getComuna() { return comuna; }
    public void setComuna(String comuna) { this.comuna = comuna; }
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    public String getNota() { return nota; }
    public void setNota(String nota) { this.nota = nota; }
}