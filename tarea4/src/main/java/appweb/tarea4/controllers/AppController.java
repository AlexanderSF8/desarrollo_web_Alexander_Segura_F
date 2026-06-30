package appweb.tarea4.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class AppController {
    
    // Cuando el usuario entre a la raíz, le entregamos el HTML
    @GetMapping("/")
    public String mostrarBuscador() {
        return "buscador"; 
    }
}