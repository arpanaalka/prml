R=ones(3,4);
R=(0.2).*R;
R(2,2)=0;
R(2,4)=-1;
R(3,4)=1;

actionm=ones(3,4);
Vpie= R;
nVpie=zeros(3,4);
iter =0;
diff=1;
u=0;
d=0;
r=0;
l=0;
while diff > .1
for j= 1:4
	for i=1:3
		a=0;b=0;
	    Vpie(2,2)=0;
	    switch i
	    case 1
		'case1';
	    	if (j==1)
		r=Vpie(i,j) + 0.8*Vpie(i,j+1) + 0.1*Vpie(i+1,j)+ 0.1*Vpie(i,j) ;
		u=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i,j+1) + 0.1*Vpie(i,j);
		d=Vpie(i,j) + 0.8*Vpie(i+1,j) + 0.1*Vpie(i,j+1)+0.1*Vpie(i,j) ; 
		l=Vpie(i,j)+0.8*Vpie(i,j+1) + 0.1*Vpie(i+1,j)+ 0.1*Vpie(i,j);
		
		elseif (j==4)
		r=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i,j) +0.1*Vpie(i+1,j);
		u=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i,j) +0.1*Vpie(i,j-1);
		d=Vpie(i,j) + 0.8*Vpie(i+1,j) + 0.1*Vpie(i,j) +0.1*Vpie(i,j-1);%=vd(i,j)
		l=Vpie(i,j) + 0.8*Vpie(i,j-1) + 0.1*Vpie(i,j) +0.1*Vpie(i+1,j); %=vl(i,j)
		
		elseif (j==2)
		r=Vpie(i,j) + 0.8*Vpie(i,j+1) + 0.1*Vpie(i,j-1)+ 0.1*Vpie(i,j); %=vr(i,j)
		u=Vpie(i,j) + 0.8*Vpie(i,j)+0.1*(Vpie(i,j-1)+Vpie(i,j+1));
		d=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*(Vpie(i,j-1)+Vpie(i,j+1));
		l=Vpie(i,j) + 0.8*Vpie(i,j-1) + 0.1*Vpie(i,j) +0.1*Vpie(i+1,j); %=vl(i,j)		
		
		else
		r=Vpie(i,j) + 0.8*Vpie(i,j+1) + 0.1*Vpie(i+1,j)+ 0.1*Vpie(i,j); %=vr(i,j)
		u=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*(Vpie(i+1,j)+ Vpie(i,j));
		d=Vpie(i,j) + 0.8*Vpie(i+1,j) + 0.1*Vpie(i,j+1)+0.1*Vpie(i,j-1);%=vd(i,j)
		l=Vpie(i,j) + 0.8*Vpie(i,j-1) + 0.1*Vpie(i,j) +0.1*Vpie(i+1,j); %=vl(i,j)
	   	end
	 
	  case 2
		'case2';
				
		if (j==1)
		r=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*(Vpie(i-1,j)+Vpie(i+1,j));
		u=Vpie(i,j) + 0.8*Vpie(i-1,j) + 0.1*Vpie(i,j) +0.1*Vpie(i,j); %vu(i,j)
		d=Vpie(i,j) + 0.8*Vpie(i+1,j) + 0.1*Vpie(i,j) + 0.1*Vpie(i,j);%=vd(i,j)
		l=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*(Vpie(i-1,j)+Vpie(i+1,j));

		elseif (j==4)
		r=Vpie(i,j) + 0.8*Vpie(i,j) +  0.1*Vpie(i-1,j) + 0.1*Vpie(i+1,j);
		u=Vpie(i,j) + 0.8*Vpie(i-1,j) + 0.1*Vpie(i,j-1) +0.1*Vpie(i,j); %vu(i,j)
		d=Vpie(i,j) + 0.8*Vpie(i+1,j) + 0.1*Vpie(i,j) + 0.1*Vpie(i,j-1);%=vd(i,j)
		l=Vpie(i,j) + 0.8*Vpie(i,j-1) + 0.1*Vpie(i-1,j) + 0.1*Vpie(i+1,j); %=vl(i,j)
		
		elseif(j==3)
		r=Vpie(i,j) + 0.8*Vpie(i,j+1) + 0.1*Vpie(i+1,j)+ 0.1*Vpie(i-1,j); %=vr(i,j)
		u=Vpie(i,j) + 0.8*Vpie(i-1,j) + 0.1*Vpie(i,j) +0.1*Vpie(i,j+1); %vu(i,j)
		d=Vpie(i,j) + 0.8*Vpie(i+1,j) + 0.1*Vpie(i,j+1)+0.1*Vpie(i,j);
		l=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i+1,j)+ 0.1*Vpie(i-1,j);
		elseif(j==2)
		r=0;
		u=0;
		d=0;
		l=0;
	  	end

	   case 3
		'case3';
		if (j==1)
		r=Vpie(i,j) + 0.8*Vpie(i,j+1) + 0.1*Vpie(i,j) + 0.1*Vpie(i-1,j); %=vr(i,j)
		u=Vpie(i,j) + 0.8*Vpie(i-1,j) + 0.1*Vpie(i,j) +0.1*Vpie(i,j+1); %vu(i,j)
		d=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i,j) +0.1*Vpie(i,j+1);
		l=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i,j) + 0.1*Vpie(i-1,j);
		
		elseif (j==4)
		r=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i-1,j)+0.1*Vpie(i,j);
		u=Vpie(i,j) + 0.8*Vpie(i-1,j) + 0.1*Vpie(i,j-1) +0.1*Vpie(i,j); %vu(i,j)
		d=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i,j-1) +0.1*Vpie(i,j);
		l=Vpie(i,j) + 0.8*Vpie(i,j-1) + 0.1*Vpie(i-1,j)+0.1*Vpie(i,j); %=vl(i,j)
		
		elseif(j==2)
		r=Vpie(i,j) + 0.8*Vpie(i,j+1) + 0.1*Vpie(i,j)+ 0.1*Vpie(i,j); %=vr(i,j)
		u=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*(Vpie(i,j-1)+Vpie(i,j+1));
		d=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*(Vpie(i,j-1)+Vpie(i,j+1));
		l=Vpie(i,j) + 0.8*Vpie(i,j+1) + 0.1*Vpie(i,j)+0.1*Vpie(i,j); %=vl(i,j)
		
		else
		r=Vpie(i,j) + 0.8*Vpie(i,j+1) + 0.1*Vpie(i,j)+ 0.1*Vpie(i-1,j); %=vr(i,j)
		u=Vpie(i,j) + 0.8*Vpie(i-1,j) + 0.1*Vpie(i,j-1) +0.1*Vpie(i,j+1); %vu(i,j)
		d=Vpie(i,j) + 0.8*Vpie(i,j) + 0.1*Vpie(i,j-1) +0.1*Vpie(i,j+1);
		l=Vpie(i,j) + 0.8*Vpie(i,j-1) + 0.1*Vpie(i-1,j)+0.1*Vpie(i,j); %=vl(i,j)
		end

	    otherwise
		disp(wrong);
	    end	
	[nVpie(i,j),actionm(i,j)] = max([r,u,l,d]);
		
	end
end
%action

nVpie(2,2)=0; %block
Vpie
nVpie
diff = norm(nVpie(:) - Vpie(:))
Vpie=nVpie;
end

Vpie
actionm
while (i!=3) && (j!=4)
		if (actionm(k,l)==1)
			c='right';
			k=k+1;
		elseif (actionm(k,l)==2)
			k=k-1;	
			c='up';
		elseif (actionm(k,l)==3)
			l=l-1;
			c='left';	
		elseif (actionm(k,l)==4)
			k=k+1;
			c='down';	
		end
	
end

