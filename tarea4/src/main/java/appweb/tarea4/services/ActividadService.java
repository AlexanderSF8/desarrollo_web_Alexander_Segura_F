package appweb.tarea4.services;

import appweb.tarea4.dto.ActividadDTO;
import appweb.tarea4.models.Actividad;
import appweb.tarea4.models.Nota;
import appweb.tarea4.repositories.ActividadRepository;
import appweb.tarea4.repositories.NotaRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

@Service
public class ActividadService {

    @Autowired
    private ActividadRepository actividadRepository;

    @Autowired
        private NotaRepository notaRepository;

    public List<ActividadDTO> buscarActividades(String keyword) {
        // Validación de seguridad en el backend: si mandan menos de 3 caracteres, devolvemos lista vacía
        if (keyword == null || keyword.trim().length() < 3) {
            return new ArrayList<>();
        }

        List<Actividad> actividadesBD = actividadRepository.buscarActividades(keyword.trim());
        List<ActividadDTO> resultados = new ArrayList<>();

        for (Actividad act : actividadesBD) {
            ActividadDTO dto = new ActividadDTO();
            dto.setId(act.getId());
            dto.setMiembroNombre(act.getMiembro().getNombre());
            dto.setDia(act.getDiasSemana());
            dto.setTipo(act.getTipo());
            dto.setComuna(act.getMiembro().getComuna().getNombre());
            dto.setDescripcion(act.getDescripcion());

            // Cálculo de la nota promedio
            if (act.getNotas() == null || act.getNotas().isEmpty()) {
                dto.setNota("-"); 
            } else {
                double suma = 0;
                for (Nota n : act.getNotas()) {
                    suma += n.getValor();
                }
                double promedio = suma / act.getNotas().size();
        
                dto.setNota(String.format(Locale.US, "%.1f", promedio)); 
            }

            resultados.add(dto);
        }

        return resultados;
    }
    // Método para guardar la evaluación
    public void agregarNota(Integer actividadId, Integer valorNota) {
        // Doble validación en el servidor 
        if (valorNota >= 1 && valorNota <= 7) {
            Actividad actividad = actividadRepository.findById(actividadId).orElse(null);
            if (actividad != null) {
                Nota nuevaNota = new Nota(valorNota, actividad);
                notaRepository.save(nuevaNota); // Guarda en MySQL mágicamente
            }
        }
    }
}