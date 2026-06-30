package appweb.tarea4.models; 

import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    // Validación exigida en la rúbrica: solo enteros entre 1 y 7
    @NotNull(message = "La nota es obligatoria")
    @Min(value = 1, message = "La nota mínima es 1")
    @Max(value = 7, message = "La nota máxima es 7")
    @Column(name = "nota", nullable = false)
    private Integer valor;

    // Relación: Muchas Notas pertenecen a Una Actividad
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actividad_id", nullable = false)
    private Actividad actividad;

    // Constructores obligatorios de JPA
    public Nota() {
    }

    public Nota(Integer valor, Actividad actividad) {
        this.valor = valor;
        this.actividad = actividad;
    }

    // Getters y Setters 
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getValor() {
        return valor;
    }

    public void setValor(Integer valor) {
        this.valor = valor;
    }

    public Actividad getActividad() {
        return actividad;
    }

    public void setActividad(Actividad actividad) {
        this.actividad = actividad;
    }
}