package appweb.tarea4.models;

import java.util.List;
import jakarta.persistence.*;

@Entity
@Table(name = "actividad")
public class Actividad {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    private String tipo;
    private String descripcion;
    
    @Column(name = "dias_semana")
    private Integer diasSemana;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "miembro_id")
    private Miembro miembro;

    // Esto es clave para calcular el promedio de notas después
    @OneToMany(mappedBy = "actividad", fetch = FetchType.LAZY)
    private List<Nota> notas;

    // Getters y Setters
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getTipo() { return tipo; }
    public void setTipo(String tipo) { this.tipo = tipo; }
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    public Integer getDiasSemana() { return diasSemana; }
    public void setDiasSemana(Integer diasSemana) { this.diasSemana = diasSemana; }
    public Miembro getMiembro() { return miembro; }
    public void setMiembro(Miembro miembro) { this.miembro = miembro; }
    public List<Nota> getNotas() { return notas; }
    public void setNotas(List<Nota> notas) { this.notas = notas; }
}