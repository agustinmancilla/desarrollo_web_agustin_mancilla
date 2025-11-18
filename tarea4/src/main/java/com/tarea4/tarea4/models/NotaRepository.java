package com.tarea4.tarea4.models;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Long> {
    
    // Usar consulta explícita porque el campo se llama aviso_id con underscore
    @Query("SELECT n FROM Nota n WHERE n.aviso_id = :avisoId")
    List<Nota> findByAviso_id(@Param("avisoId") Integer avisoId);
}
