package appweb.tarea4.repositories;

import appweb.tarea4.models.Actividad;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ActividadRepository extends JpaRepository<Actividad, Integer> {

    @Query("SELECT a FROM Actividad a WHERE " +
           "LOWER(a.miembro.nombre) LIKE LOWER(CONCAT('%', :keyword, '%')) OR " +
           "LOWER(a.descripcion) LIKE LOWER(CONCAT('%', :keyword, '%')) OR " +
           "LOWER(a.miembro.comuna.nombre) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<Actividad> buscarActividades(@Param("keyword") String keyword);
}