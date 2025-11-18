package com.tarea4.tarea4.models;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Email;
import jakarta.persistence.Enumerated;
import jakarta.persistence.EnumType;
@Entity
@Table
public class Aviso_adopcion {
    @Id
    @SequenceGenerator(
        name = "aviso_adopcion_sequence",
        sequenceName = "aviso_adopcion_sequence",
        allocationSize = 1
    )
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "aviso_adopcion_sequence")
    private Long id;
    
    @NotNull
    private LocalDateTime fecha_ingreso;

    @NotNull
    private Integer comuna_id;

    private String sector;

    @NotNull
    private String nombre;

    @NotNull
    @Email
    private String email;

    private String celular;

    @NotNull
    @Enumerated(EnumType.STRING)
    private TipoAnimal tipo;

    @NotNull
    private Integer cantidad;

    @NotNull
    private Integer edad;

    @NotNull
    @Enumerated(EnumType.STRING)
    private UnidadMedida unidad_medida;

    @NotNull
    private LocalDateTime fecha_entrega;

    private String descripcion;

    public enum TipoAnimal {
        gato, perro
    }

    public enum UnidadMedida {
        a, m  
    }

    public Aviso_adopcion() {
    }   

    public Long getId() {
        return id;
    }
    
    public LocalDateTime getFecha_ingreso() {
        return fecha_ingreso;
    }
    public Integer getComuna_id() {
        return comuna_id;
    }
    public String getSector() {
        return sector;
    }
    public String getNombre() {
        return nombre;
    }
    public String getEmail() {
        return email;
    }
    public String getCelular() {
        return celular;
    }
    public TipoAnimal getTipo() {
        return tipo;
    }
    public Integer getCantidad() {
        return cantidad;
    }
    public Integer getEdad() {
        return edad;
    }
    public UnidadMedida getUnidad_medida() {
        return unidad_medida;
    }
    public LocalDateTime getFecha_entrega() {
        return fecha_entrega;
    }
    public String getDescripcion() {
        return descripcion;
    }
}