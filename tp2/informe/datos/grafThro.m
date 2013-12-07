function A = graf(s,t)

        A = load(s);
        n = size(A,1);

        xmin = floor(min((min(A(:,1))))) - 5;
        xmax = ceil(max((max(A(:,1))))) + 25;
        ymin = floor(min((min(A(:,[2,3,4,5])))));
        ymax = ceil(max((max(A(:,[2,3,4,5]))))) + 2;
        
        plot(A(:,1),A(:,2),"1");
        hold on;
        plot(A(:,1),A(:,3),"2");
        hold on;
        plot(A(:,1),A(:,4),"3");
        hold on;
        plot(A(:,1),A(:,5),"4");
        axis([xmin xmax ymin ymax]);
        xlabel('tamano del archivo');
        ylabel('transferencia en kb/s');
        legend('SEND WINDOW 1','SEND WINDOW 10', 'SEND WINDOW 15', 'SEND WINDOW 20');
        title(t)
        hold off;
end
        
 
