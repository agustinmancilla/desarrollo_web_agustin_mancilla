package com.tarea4.tarea4.models;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table
public class Nota {
    @Id
    @SequenceGenerator(
        name = "nota_sequence",
        sequenceName = "nota_sequence",
        allocationSize = 1
    )
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "nota_sequence")
    private Long id;

    @NotNull
    private Integer aviso_id;

    @NotNull
    private Integer nota;

    public Nota() {
    }

    public Nota(Integer aviso_id, Integer nota) {
        this.aviso_id = aviso_id;
        this.nota = nota;
    }

    public Long getId() {
        return id;
    }

    public Integer getAviso_id() {
        return aviso_id;
    }

    public Integer getNota() {
        return nota;
    }

    public static Boolean ValidateNota(Integer nota) {
        return nota != null && nota >= 1 && nota <= 7;
    }
}