package appweb.tarea4.controllers;

import appweb.tarea4.dto.ActividadDTO;
import appweb.tarea4.services.ActividadService;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
public class ApiController {
    
    private final ActividadService actividadService;

    // Inyección de dependencias 
    public ApiController(ActividadService actividadService) {
        this.actividadService = actividadService;
    }

    // Endpoint del buscador
    @GetMapping("/api/actividades/{keyword}")
    public Map<String, List<ActividadDTO>> buscarActividades(@PathVariable("keyword") String keyword) {
        List<ActividadDTO> resultados = actividadService.buscarActividades(keyword);
        return Map.of("data", resultados); 
    }

    // Endpoint para evaluar (Recibe un JSON con la nota)
    @PostMapping("/api/actividades/{id}/evaluar")
    public Map<String, String> evaluarActividad(@PathVariable("id") Integer id, @RequestBody Map<String, Integer> payload) {
        Integer nota = payload.get("nota");
        actividadService.agregarNota(id, nota); 
        return Map.of("status", "ok");
    }
}