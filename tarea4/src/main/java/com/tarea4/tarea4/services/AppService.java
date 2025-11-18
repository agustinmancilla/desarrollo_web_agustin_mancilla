package com.tarea4.tarea4.services;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;
import java.nio.file.Path;

import com.tarea4.tarea4.models.Aviso_adopcion;
import com.tarea4.tarea4.models.Comuna;
import com.tarea4.tarea4.models.Nota;
import com.tarea4.tarea4.models.AvisosRepository;
import com.tarea4.tarea4.models.ComunaRepository;
import com.tarea4.tarea4.models.NotaRepository;


@Service
public class AppService {
    private final String pathStatic;
    private final AvisosRepository avisoRepository;
    private final ComunaRepository comunaRepository;
    private final NotaRepository notaRepository;

    public AppService(AvisosRepository avisoRepository, ComunaRepository comunaRepository, NotaRepository notaRepository) throws IOException {
        this.avisoRepository = avisoRepository;
        this.comunaRepository = comunaRepository;   
        this.notaRepository = notaRepository;
        
        Path staticDir = Paths.get(ResourceUtils.getFile("classpath:static").getAbsolutePath());
        this.pathStatic = staticDir.toString();
        System.out.println("Static path resolved to: " + this.pathStatic);
    }

    public List<Map<String, String>> getAvisosData() {
    List<Aviso_adopcion> avisos = avisoRepository.findAllByOrderByIdDesc(Pageable.unpaged()).getContent();
    List<Map<String, String>> avisosData = new ArrayList<>();
    
    for (Aviso_adopcion aviso : avisos) {
        Map<String, String> avisoData = new HashMap<>();
        
        
        avisoData.put("id", aviso.getId().toString());
        avisoData.put("fecha_publicacion", aviso.getFecha_ingreso().toLocalDate().toString() );
        avisoData.put("sector", aviso.getSector());
        avisoData.put("cantidad", aviso.getCantidad().toString());
        avisoData.put("tipo", aviso.getTipo().toString());
        avisoData.put("edad", aviso.getEdad().toString());
        avisoData.put("unidad_medida", aviso.getUnidad_medida().toString());
        
        
        
        
        String nombreComuna = getNombreComuna(aviso.getComuna_id());
        avisoData.put("comuna", nombreComuna);
        
        
        Double promedio = getPromedioNotas(aviso.getId());
        avisoData.put("promedio_notas", String.format("%.2f", promedio));
        
        avisosData.add(avisoData);
        }
    
    return avisosData;
    }


    public String getNombreComuna(Integer comunaId) {
        if (comunaId == null) {
            return "Comuna no especificada";        
        }
        return comunaRepository.findById(comunaId.longValue())
                              .map(Comuna::getNombre)
                              .orElse("Comuna no encontrada");
    }
    
    public Double getPromedioNotas(Long avisoId) {
        if (avisoId == null) {
            return null;
        }
        List<Nota> notas = notaRepository.findByAviso_id(avisoId.intValue());
        if (notas == null || notas.isEmpty()) {
            return null;
        }
        return notas.stream()
                   .mapToDouble(nota -> nota.getNota().doubleValue())
                   .average()
                   .orElse(0.0);
    }
    
    public boolean guardarNota(Integer avisoId, Integer nota) {
        if (!Nota.ValidateNota(nota)) {
            return false;
        }
        try {
            Nota nuevaNota = new Nota(avisoId, nota);
            notaRepository.save(nuevaNota);
            return true;
        } catch (Exception e) {
            System.err.println("Error al guardar nota: " + e.getMessage());
            return false;
        }
    }
}
