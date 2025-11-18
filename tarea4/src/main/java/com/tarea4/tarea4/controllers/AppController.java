package com.tarea4.tarea4.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.ui.Model;
import com.tarea4.tarea4.services.AppService;
import java.util.List;
import java.util.Map;
@Controller
public class AppController {
    private final AppService appService;
    public AppController(AppService appService) {
        this.appService = appService;
    }
    
    @GetMapping("/")
    public String mostrarTablaAvisos(Model model) {
        List<Map<String, String>> avisosData = appService.getAvisosData();
        model.addAttribute("avisos", avisosData);
        return "evaluacion";
    }
    
    @PostMapping("/evaluar")
    public String evaluarAviso(@RequestParam("avisoId") Integer avisoId, 
                          @RequestParam("nota") Integer nota) {
        appService.guardarNota(avisoId, nota);
        return "redirect:/";
    }
}
